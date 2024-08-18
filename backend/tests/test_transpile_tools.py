import unittest
import sqlglot
import transpile_tools as trans


class TestSqlCustomTranspilation(unittest.TestCase):
    def test_multiple_space(self):
        # hive to presto
        input_dialect = "hive"
        output_dialect = "presto"
        input_sql = "select  arr[0] "  # two space in the middle, and one at last
        output_sql = sqlglot.transpile(input_sql, read=input_dialect, write=output_dialect, identify=False, pretty=True)[0]
        customized_sql = trans.customized_transpile(input_sql, input_dialect
                                                    , output_sql, output_dialect)
        expected_sql = "select  arr[1] "
        self.assertEqual(customized_sql, expected_sql)
        
    def test_single_line_commend(self):
        # hive to presto
        input_dialect = "hive"
        output_dialect = "presto"
        input_sql = "select arr[0]  -- first element of array"  # two space
        output_sql = sqlglot.transpile(input_sql, read=input_dialect, write=output_dialect, identify=False, pretty=True)[0]
        customized_sql = trans.customized_transpile(input_sql, input_dialect
                                                    , output_sql, output_dialect)
        expected_sql = "select arr[1]  -- first element of array"
        self.assertEqual(customized_sql, expected_sql)
        
    def test_multiple_line_commend(self):
        # hive to presto
        input_dialect = "hive"
        output_dialect = "presto"
        input_sql = """ 
            /*
            database: dev
            table: student
            columns: id, name, class
            */
            select 
                id, name, class, interest_group[0]
            from dev.student"""
        output_sql = sqlglot.transpile(input_sql, read=input_dialect, write=output_dialect, identify=False, pretty=True)[0]
        customized_sql = trans.customized_transpile(input_sql, input_dialect
                                                    , output_sql, output_dialect)
        expected_sql = """ 
            /*
            database: dev
            table: student
            columns: id, name, class
            */
            select 
                id, name, class, interest_group[1]
            from dev.student"""
        self.assertEqual(customized_sql, expected_sql)
        
        
        