pip install s3cmd
cp ./hw2/.s3cfg /home/ubuntu/
cd hw2
s3cmd put s3://jakes-dsc-291-bucket/*.txt .
python3 TestLatencies.py