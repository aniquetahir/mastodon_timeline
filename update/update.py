#!/usr/bin/env python3

import pandas as pd
import requests
import datetime as dt
import pyarrow.parquet as pq
import pyarrow as pa
import os

STATE_FILENAME = 'data/timeline.parquet'
DIRECTORY_FILENAME = 'data/directory.parquet'
TOKEN = os.environ['INSTANCES_SOCIAL_TOKEN'].strip()

def type_instances(dfi):
    """
    Set the right types for relevant columns
    """
    
    for col in ['users', 'statuses']:
        dfi[col] = dfi[col].astype(int)
    dfi.updated_at = pd.to_datetime(dfi.updated_at)
    return dfi

def filter_instances(dfi):
    """
    Filter out instances that
    - return negative `users` or `statuses`
    - return NaN update times
    - update times an hour before or after the median update time
    """
    
    dfi = dfi[(dfi.users >= 0) & (dfi.statuses >= 0) & (dfi.updated_at.notna())]
    dfi = dfi[(dfi.updated_at > (median_time - dt.timedelta(hours=1))) | (dfi.updated_at < (median_time + dt.timedelta(hours=1)))]
    return dfi

def get_instances():
    """
    Download instance data from instances.social
    """
    
    url = 'https://instances.social/api/1.0/instances/list?count=0&include_down=false'
    headers = {"Authorization": f'Bearer {TOKEN}'}
    response = requests.get(url, headers=headers, timeout=20)
    response = response.json()
    return pd.DataFrame(response['instances'])    

def prepare_state(dfi):
    """
    Select columns, collapse update times to a single value for better file compression
    """
    
    state = dfi[['id', 'users', 'statuses']]
    state.insert(0, 'update_at', median_time.replace(second=0, microsecond=0))
    return state

def save_timeline(state):
    """
    Join the current with all previous states and save as a parquet
    """
    
    old = pq.read_table(STATE_FILENAME).to_pandas()
    timeline = pd.concat([old, state])
    pq.write_table(pa.Table.from_pandas(timeline), STATE_FILENAME, use_deprecated_int96_timestamps=True)

def save_directory(instances):
    """
    Save a simple directory table of instance id-name pairs
    """
    
    directory = instances[['id', 'name']]
    old = pq.read_table(DIRECTORY_FILENAME).to_pandas()
    directory = pd.concat([old, directory]).drop_duplicates(subset=['id'], keep='last')
    pq.write_table(pa.Table.from_pandas(directory), DIRECTORY_FILENAME)


instances = get_instances()
instances = type_instances(instances)
median_time = instances.updated_at.median()
instances = filter_instances(instances)
state = prepare_state(instances)
save_timeline(state)
save_directory(instances)
