from pyspark.sql import functions
import re

def match_levenshtein(spark, match_name, input_col, provider_name, match_col, distance):
    def join(input, provider_data):
        if not (provider_name in provider_data):
            raise RuntimeError("Missing provider: " + provider_name)
        data = provider_data[provider_name]
        new_column_name_list = list(map(lambda x: match_name + "__" + x, data.columns))
        data = data.toDF(*new_column_name_list)
        fq_match_col = match_name + "__" + provider_name + "__" + match_col
        expression = functions.levenshtein(input[input_col], data[fq_match_col]) < distance
        return data.join(functions.broadcast(input), expression, how="right")
    return join

def match_soundex(spark, match_name, input_col, provider_name, match_col):
    def join(input, provider_data):
        if not (provider_name in provider_data):
            raise RuntimeError("Missing provider: " + provider_name)
        data = provider_data[provider_name]
        new_column_name_list = list(map(lambda x: match_name + "__" + x, data.columns))
        data = data.toDF(*new_column_name_list)
        fq_match_col = match_name + "__" + provider_name + "__" + match_col
        expression = functions.soundex(input[input_col]) == functions.soundex(data[fq_match_col])
        return data.join(functions.broadcast(input), expression, how="right")
    return join

def match_contains(spark, match_name, input_col, provider_name, match_col):
    def join(input, provider_data):
        if not (provider_name in provider_data):
            raise RuntimeError("Missing provider: " + provider_name)
        data = provider_data[provider_name]
        new_column_name_list = list(map(lambda x: match_name + "__" + x, data.columns))
        data = data.toDF(*new_column_name_list)
        fq_match_col = match_name + "__" + provider_name + "__" + match_col
        expression = functions.expr(fq_match_col + " LIKE concat('%', " + input_col + ", '%')")
        return data.join(functions.broadcast(input), expression, how="right")
    return join

def resolve(spark, input_file, providers, matchers):
    input = spark.read.csv(input_file, header=True)
    provider_data = { provider: spark.read.csv(file, header=True)
                      for provider, file in providers.items() }
    for matcher in matchers:
        input = matcher(input, provider_data)
    return input
