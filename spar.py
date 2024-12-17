from pyspark.sql import SparkSession

# 创建Spark会话 (SparkSession)
spark = SparkSession.builder.master("local").appName("SimpleApp").getOrCreate()

# 创建一个DataFrame
data = [("Alice", 1), ("Bob", 2), ("Cathy", 3)]
columns = ["name", "value"]
df = spark.createDataFrame(data, columns)

# 显示DataFrame内容
df.show()

# 对DataFrame进行简单操作：过滤出 value > 1 的行
filtered_df = df.filter(df.value > 1)

# 显示过滤后的结果
filtered_df.show()

# 停止Spark会话
spark.stop()
