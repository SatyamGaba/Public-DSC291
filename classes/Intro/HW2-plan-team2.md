# HW2 plan for Team-2 DSC291

### Background
Data transfer between nodes of distributed systems can become a potential bottleneck of big data applications, especially when computing resources and memory resources are not co-located. It is important to understand the performance differences that the system's interfaces afford, and the price one pays to utilize them. In this experiment, we will analyze how long it takes to transfer different loads of data from the S3 storage service to different EC2 instances and how instance pricing is related to data transfer performance. 

### Approach
We are going to start with a script making use of the AWS-Jupyter package. As four of our members have successfully set up AWS-Jupyter, we are going to do a Zoom meeting with one of them screen-sharing a draft notebook in the cloud. We will then try to come up with a script that can measure performance across multiple instances many times. This will be run in the cloud once, and the resulting data will be saved in our github. Statistical analysis of the results can then be done locally. The final result will be a Jupyter notebook presentation that includes both the code for running the experiment and for the statistical analysis.

### Data
We have not yet decided which data we will be using, but there’s a lot of stuff publicly available on AWS at https://registry.opendata.aws/. A cool example could be Sentinel 2 satellite data; There’s more than 1 PB of that data out there, and it’s all openly available through AWS. 
