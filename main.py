import argparse
import csv
import json
import sys
from pathlib import Path


def convert_csv_to_json(input_path, output_path):
    """Convert CSV to JSON"""
    try:
        with open(input_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]

        # Convert numeric values
        for row in data:
            for key, value in row.items():
                row[key] = convert_value(value)

        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    except FileNotFoundError:
        sys.exit(f"Error: Input file {input_path} not found")
    except csv.Error as e:
        sys.exit(f"CSV parsing error: {str(e)}")


def convert_json_to_csv(input_path, output_path):
    """Convert JSON to CSV"""
    try:
        with open(input_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            sys.exit("Error: JSON data should be an array of objects")

        # Get fieldnames from the first object
        fieldnames = list(data[0].keys()) if data else []

        with open(output_path, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    except FileNotFoundError:
        sys.exit(f"Error: Input file {input_path} not found")
    except json.JSONDecodeError:
        sys.exit("Error: Invalid JSON format")
    except KeyError as e:
        sys.exit(f"Missing key in JSON data: {str(e)}")


def convert_value(value):
    """Convert string values to appropriate data types"""
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value


def main():
    parser = argparse.ArgumentParser(
        description="File Format Converter - CSV/JSON互转工具",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'mode',
        choices=['csv2json', 'json2csv'],
        help='转换模式:\n'
             '  csv2json - 将CSV转换为JSON\n'
             '  json2csv - 将JSON转换为CSV'
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='输入文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='输出文件路径'
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        sys.exit(f"错误：输入文件 {input_path} 不存在")

    try:
        if args.mode == 'csv2json':
            convert_csv_to_json(input_path, output_path)
        elif args.mode == 'json2csv':
            convert_json_to_csv(input_path, output_path)
        print(f"转换成功！输出文件：{output_path}")
    except Exception as e:
        sys.exit(f"转换过程中发生错误: {str(e)}")


if __name__ == '__main__':
    main()
