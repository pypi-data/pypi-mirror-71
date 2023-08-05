# metasheet

A Python library for generating metadata around statsitcial and scientific datasets in various formats from an Excel or Google spreadsheet. Primarily intended for use with various MTNA packages or DDI aware tools.

This package requires Python 3.

## How it works

Each sheet in the workbook is used to describe a particular type of resource, currently classification, code, variable, record, layout. Rule will be added shortly.

Each column in the sheet maps to a particular resource property. The column header row is used to detemerine such correspondence. The name in the sheet may be different from the actual property name, and these mappings are defined in a JSON configuration file using regular expressions. A default configuration is provided as a recommended version, but this can be customized. Colums for which no mapping is found are ignored.

### Running the tools

From the metasheet directory, run

`python metasheet -h`

```bash
usage: metasheet.py [-h] [-c CONFIG] [-a] [-bq] [-ddi 2.5|3.1] [-pandas] [-rds]
                    [-rml] [-sts]
                    excel_file
```

Currently supported formats include:

* bq: To generate a table for hosting data in Google Big Query
* ddi: Various versions/flavors of DDI-XML (can be used with SledgeHammer)
* rds: JSON format used by MTNA Rich Data Services
* rml: a low level syntax used by MTNA Atua framework
* sts: Stat/Transfer syntax that can be used with MTNA SledgeHammer for reading data
* vertica: SQL syntax to create tables in HP Vertica

Use ```-a``` to generate all possible outputs.

Note that this package requires Python version 3 (may work with 2).

### Configuration

The package is driven by a configuration file that maps the sheet names and columns into resources and properties. This usually does not need to be changed unless you use custome properties. See default [```config.json```](metasheet/config.json)metasheet/config.json] in package source.

The configuration file provides metasheet with the information it needs to process the worksheet. This includes:

* ```sheetRegex```: this regular expression, specified for each resources type,  is used to match a sheet name with the particular type. For example, ```"sheetRegex":"^variable.*"``` is the defualt used to match variabel sheets.
* ```propertyMaps```: holds information about mappin columns header names to resource properties. Property maps can be specified at the resource type or global level (in which case they apply to all resources. See below for 

#### Property Maps

A property maps matches a sheet column with a specific resource property. This is use to allow different names to be used in the sheets (rather than restricting to a list of internal names). Property maps can exist at the global or resource type level, the later taking precedence. 

A recource map must contain the following elements:

* regex: the regular expression that the column header name is matching. 
* property: the internal property name

Optional elements can be included to suport specific serializers (e.g. rml, rds, etc.)

For example:

```{"regex":"abbr|abbreviation","property":"name[abbreviation]","rml":"*"},```

maps the ```abbr``` or ```abbreviation``` column into the property ```name[abbreviation]```

Note that for faceted properties, a special "named" search group is introduced to determine the facet components. In Python, this takes the form ```?P<facets>``` as a group prefix. The following for example maps a ```name``` column into the into ```name``` property but would also map name[label] into ```name[label]```
```{"regex":"^name(\\[(?P<facets>.*)\\])?$","property":"name"}```

Note that the Layout resource type also inherits all the properties of the variable type.◊

## Resources

All resources have a ```uid``` property generated as a UUID

The following properties can be associated with any resource (not all being relevant to all recources):

* ```name[abbreviation]```: the container this resource will be stored in* ```bank```: the container that "defines / holds this resource. Every resource belongs to a bank (implicitely or explicitely).
* ```basis```: a reference to a resource of the same type from which properties can be inherited. 
* ```clbank```: a classfication bank identifer
* ```id```: the resource identifier (must be unique in the workbook or bank)
* ```name```: the resource name

In most cases, the ```id``` and ```name``` are the same so specifying only one of them is typically sufficient.

Additional serialzier specific map properties can also be used. For example:

* ```rml```: If present, indicates that this property should be set on RML resources. A "*" indicates that the RML property has the same name. 
* ```rds```: If present, indicates that this property should be set on RDS resources. A "*" indicates that the RML property has the same name. 

### References

A reference to another resource must be unique within the worksheet to ensure proper resolution (). References can be specified in various ways, usually using two properties representing a ```bank``` and an ```id```, or using the dot notation like ```bank.id```.

### Inheritance

The ```basis``` property on a resourceis a reference to another resource of the same type whose properties are inherited if not locally specified.

### Facets

Certain properties can be faceted, this includes ```name```, ```description```, ```dataType```, and more. 


## Classifications

A classification is composed of the classification definition and its code list. These are captured in two seperate sheets.

### Classification

The following properties are specific to the Classification:

* n/a

### Code

The following properties are specific to the Code:

* ```classification```: the classification the code belongs to
* ```value```: The code value 

## Variables

Variable must have at least a ```name```, a ```bank```, and typically a datatype.

The following properties are specific to the Variable:

* ```classification```: a reference to the classification used by this variable
* ```datatype```: a generic or faceted data type 
* ```decimals```: for numeric variables, the number of digits after the decimal point (0 implies integer)
* ```end```: the end column position when used in a record layout serialized in fixed ASCII
* ```profile```: ?
* ```start```: the start column position when used in a record layout serialized in fixed ASCII
* ```units```: a list generic or faceted units relevant for this variable (observation, analysis)
* ```width```: the total width of the variable content (e.g. for storing data in a fixed width ASCII file)

## Record Layout

A record layout has two components/sheets: Record and Layout

### Record

Capture properties for entire record layout 

Required elements are: ```bank```, ```id```, ```name```

The following properties are specific to the Record:

* ```varbank```: a default variable bank id that applies to all variables in the layout
* ```unit```: one or more record unit types (semi-colon separated)
* ```pk|primary```: one or more variables defining the record primary key. Compound keys variables are separate with a "+".
* ```fk|foreign```: one or more sets of variable(s) defining the record foreigns keys. Compound keys variables are separate with a "+", and multiple keys are separated by a ";".

### Layout

A Layout create or add variable to a record 

Variables can be either locally created or included by reference (if no additional properties are required for the record layout). This is determined by the presence of certain properties. If no other properties than the record and variable are specified, the variable in included by references. Otherwise it is locally defined. A layout technically mix both.

The following properties are specific to the Layout:

* ```variable```: the base variable identifier
* ```varbank```: the variable bank holding the referenced variable. This can override the record level varbank.
* ```rlbank```: the bank holding the record 
* ```record```: the record identifier

In addition, all the properties supported by the Variable resource can also be used (e.g. to locally define a variable)

For a Layout, the basis property (if not set) is automatically inferred from the variable and varbank properties.

## Rules

Rules are used by the MTNA Atua framework quality assurance and ETL components, and mainly used at this time by our Resource Modeling Language (RML) serializer. Consult the RML documentation to better understand how the rules works and their syntax. 

The following properties are specific to the Layout

* ```resource```: the resource the rule applies to (may be supplemented by a bank properity)
* ```assert```: the expression statement to test
* ```condition```: the condition under which the rule applies
* ```onFail```: the action to take when the rule assertion fails
* ```onSuccess```: the action to take when the rule assertion succeeds
* ```contextVariables```: a comma separate list of variables whose values will be reported with the onPass/onFail messages

Note that rules do not require an unique identifier at this time. 
