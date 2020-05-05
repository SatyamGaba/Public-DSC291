#!/bin/bash
pip install s3cmd
cd hw2
/home/ubuntu/.local/bin/s3cmd get s3://jakes-bucket-dsc-291/*.csv ./hw2 --access_key= --secret_key= --region us-west-2 --force
python3 TTestLatencies.py