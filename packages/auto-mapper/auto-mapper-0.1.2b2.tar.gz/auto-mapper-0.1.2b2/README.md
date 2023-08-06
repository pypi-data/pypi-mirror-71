# Auto Mapper

A package that **maps** a set of strings to another set of objects where each object is described as:
```python
{
  'code': 'unique_code',
  'name': 'given name'
}
```

## How it works
Tha process mainly starts by a text-cleaning, which is just another way of saying text processing, with the help of certain dependencies ([NLTK](https://www.nltk.org/) for the current release).
\
The cleaning operation transforms each string to a list of tokens. By running a text similarity algorithm on the resulting vectors we're able to map certain fields with the most similar columns.
\
Another phase of mapping consist of an additional text processing step, which is `stemming`, combined with a lower similarity threshold is applyed on the unmapped fields.
\
The final step is to measure the semantic similarity between the unmapped fields and columns. Thanks to [Datamuse](http://datamuse.com) and their greate API we were able to ~externalize this operation.

## Installation
First you need to install the package, then run a setup script that will download the necessary ntlk packages
```
$ pip install auto-mapper
$ setup-nltk
```

`NOTE:` if you are using a virtual environment, please check it out before running the nltk setup **It downloads the packages to the environment folder**

## Usage
It's pretty straightforward
```pycon
>>> from mapper import AutoMapper
>>> mapper = AutoMapper()
>>> cols = ['city', 'Location Name']
>>> fields = [{'code': 'loc_name', 'name': 'location names'}, {'code': 'town', 'name': 'Town'}]
>>> mapping_result, unmapped_columns_indices, unmapped_fields_indices = mapper.map(column_names=cols, fields=fields)
>>> print(mapping_result)
[{'source': ['city'], 'target': 'town'}, {'source': ['Location Name'], 'target': 'loc_name'}]
>>> print(unmapped_columns_indices)
set()
>>> print(unmapped_fields_indices)
set()
```