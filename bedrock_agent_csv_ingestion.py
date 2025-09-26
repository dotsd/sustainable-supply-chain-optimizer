import boto3
import json
from typing import Dict, Any

class BedrockAgentCSVIngestion:
    def __init__(self):
        self.glue_client = boto3.client('glue')
        self.s3_client = boto3.client('s3')
    
    def lambda_handler(self, event: Dict[str, Any], context) -> Dict[str, Any]:
        """Main handler for Bedrock Agent"""
        action = event.get('actionGroup', '')
        function = event.get('function', '')
        
        if function == 'ingest_csv_files':
            return self.ingest_csv_files(event.get('parameters', {}))
        
        return {
            'response': {
                'actionGroup': action,
                'function': function,
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': 'Function not supported'
                        }
                    }
                }
            }
        }
    
    def ingest_csv_files(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest CSV files from S3 to Glue table"""
        try:
            bucket_name = parameters.get('bucket_name')
            csv_prefix = parameters.get('csv_prefix', '')
            database_name = parameters.get('database_name')
            table_name = parameters.get('table_name')
            
            # Create Glue database if not exists
            try:
                self.glue_client.create_database(
                    DatabaseInput={'Name': database_name}
                )
            except self.glue_client.exceptions.AlreadyExistsException:
                pass
            
            # Create Glue table
            table_input = {
                'Name': table_name,
                'StorageDescriptor': {
                    'Columns': [
                        {'Name': 'col1', 'Type': 'string'},
                        {'Name': 'col2', 'Type': 'string'},
                        # Add more columns as needed
                    ],
                    'Location': f's3://{bucket_name}/{csv_prefix}',
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                        'Parameters': {
                            'field.delim': ',',
                            'skip.header.line.count': '1'
                        }
                    }
                }
            }
            
            self.glue_client.create_table(
                DatabaseName=database_name,
                TableInput=table_input
            )
            
            response_text = f"Successfully created Glue table {table_name} for CSV files in s3://{bucket_name}/{csv_prefix}"
            
        except Exception as e:
            response_text = f"Error ingesting CSV files: {str(e)}"
        
        return {
            'response': {
                'actionGroup': 'csv_ingestion',
                'function': 'ingest_csv_files',
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': response_text
                        }
                    }
                }
            }
        }

# Lambda function entry point
def lambda_handler(event, context):
    agent = BedrockAgentCSVIngestion()
    return agent.lambda_handler(event, context)