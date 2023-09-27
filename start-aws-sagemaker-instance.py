import boto3
import time

# Replace these variables with your specific values
instance_name = "ext-efs-8A100"
max_retries = 50

sagemaker = boto3.client("sagemaker")

for i in range(max_retries):
    try:
        response = sagemaker.start_notebook_instance(
            NotebookInstanceName=instance_name
        )
        print(f"Attempt {i + 1}: Started SageMaker notebook instance {instance_name}")

        status = sagemaker.describe_notebook_instance(
            NotebookInstanceName=instance_name
        )

        while status['NotebookInstanceStatus'] == 'Pending':
            print('Status of Notebook: Pending')
            time.sleep(30)

        if status['NotebookInstanceStatus'] == 'Failed':
            print(f"{status['InstanceType']} failed with a Failure Reason: {status['FailureReason']}")
            if i < max_retries - 1:
                print("Retrying in 30 seconds...")
                time.sleep(30)
        elif status['NotebookInstanceStatus'] == 'Inservice':
            print('Notebook in Service!!!!!')
            break
    except Exception as e:
        print(f"Attempt {i + 1}: Failed to start instance: {str(e)}")
        if i < max_retries - 1:
            print("Retrying in 30 seconds...")
            time.sleep(30)
        else:
            print("Maximum retry attempts reached. Instance could not be started.")
