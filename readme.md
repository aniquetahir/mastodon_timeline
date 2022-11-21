User and status counts for each mastodon instance from [instances.social](https://instances.social) queried every 3 hours since November 4, 2022.

[Browse on observablehq](https://observablehq.com/@mauforonda/what-goes-on-in-mastodon)

- All data is consolidated in [timeline.parquet](data/timeline.parquet)
- Some convenient csv views:
  - [a timeseries for all users and statuses](data/mastodon.csv)
  - [the latest count for each instance](data/instances.csv)
  - [a timeseries for each instace](data/instance)
  
Some notes:
- On November 21, 2022, [instances.social](https://github.com/TheKinrar/instances/) [changed](https://mastodon.xyz/@TheKinrar/109381846167480060) fixed how new instances are discovered and indexed. For a few hours the numbers it reported are weird, featuring instances that deliberately publish wrong numbers and many duplicates. After [this commit](https://github.com/mauforonda/mastodon_timeline/commit/1e3a804565f82495c7e3a8ccb3906b780a6f157b) I expect things to go much more smoothly. The number of instances I indexed in this repository grew from 1904 to 11,115 and the number of users from 4,797,132 to 6,023,097. These new numbers should reflect much better the state of the mastodon ecosystem.
