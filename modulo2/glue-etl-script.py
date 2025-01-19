import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1736894447778 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://897722708429-raw/b3-portfolio.parquet"], "recurse": True}, transformation_ctx="AmazonS3_node1736894447778")

# Script generated for node Drop Duplicates
DropDuplicates_node1736894583598 =  DynamicFrame.fromDF(AmazonS3_node1736894447778.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1736894583598")

# Script generated for node Aggregate
Aggregate_node1736894717018 = sparkAggregate(glueContext, parentFrame = DropDuplicates_node1736894583598, groups = ["Codigo", "Acao", "Tipo", "QuantTeorica", "Partic", "Data"], aggs = [["QuantTeorica", "sum"], ["Data", "max"]], transformation_ctx = "Aggregate_node1736894717018")

# Script generated for node Rename Field
RenameField_node1737244902551 = RenameField.apply(frame=Aggregate_node1736894717018, old_name="`sum(QuantTeorica)`", new_name="SomaQuantidade Teorica", transformation_ctx="RenameField_node1737244902551")

# Script generated for node Rename Field
RenameField_node1737245220222 = RenameField.apply(frame=RenameField_node1737244902551, old_name="`max(Data)`", new_name="DataMaxima", transformation_ctx="RenameField_node1737245220222")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=Aggregate_node1736894717018, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1736894434565", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1736894888566 = glueContext.getSink(path="s3://897722708429-refined", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1736894888566")
AmazonS3_node1736894888566.setCatalogInfo(catalogDatabase="pos-tech",catalogTableName="fiap-mlet3")
AmazonS3_node1736894888566.setFormat("glueparquet", compression="snappy")
AmazonS3_node1736894888566.writeFrame(Aggregate_node1736894717018)
job.commit()