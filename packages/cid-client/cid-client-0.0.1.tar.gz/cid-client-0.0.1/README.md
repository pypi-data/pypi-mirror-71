# Client for Coherent Identifier Tool

Wrapper for [CID Tool GraphQL API](https://github.com/coherentdigital/coherent-identifier/tree/cid-oleg-new/cid_tool).

## Usage

    pip install cid-client    
    
## Authentication

Basic (login/password) authentication with limited number of service users is currently used in CID Tool.
Service and test credentials are available in AWS SecretManager.

```python
from cid_client import authenticate_basic
auth = authenticate_basic('<your login>', '<your password>')
access_token = auth['accessToken']
```

Access token is then used for any Create/Update of the CID.


## Code examples

Find all examples: [here](examples).

**CID create:**

```python
from cid_client import create_cid
import json
from cid_client.mapping_inputs import *


"""
    See full list of possible input things in mapping_inputs.py.
    Create CID allows you to supply primary info.
    
    who: PersonOrThingInput
    what: ThingInput
    where: PlaceInput
    location: LocationInput
    props: List[PropertyValueInput]
    
    Absolute minimal info for CID creation is an artifact HTTP link.
    Alternatively (or additionally) you can supply representation images. 
"""

cid_input = CreateCIDInput(
    who=PersonOrThingInput(
        thing=ThingInput(
            name='CID Harverter'
        )
    ),
    location=LocationInput(
        artifact='https://www.osha.gov/Publications/OSHA3990.pdf'
    )
)

record_with_id = create_cid(cid_input, access_token='<your token here>')
print(json.dumps(record_with_id, indent=2))
```


**CID Update**

```python
from cid_client import update_cid
import json
from cid_client.mapping_inputs import *

"""
    See full list of possible input things in mapping_inputs.py.
    Create CID allows you to supply primary info.

    who: PersonOrThingInput
    what: ThingInput
    where: PlaceInput
    location: LocationInput
    props: List[PropertyValueInput]

    Absolute minimal info for CID creation is an artifact HTTP link.
    Alternatively (or additionally) you can supply representation images. 
"""

cid_input = UpdateCIDInput(
    cid='20.500.12592/s4mww0',
    location=LocationInput(
        representation=['https://media.graytvinc.com/images/810*455/Coronavirus_MGN_CDC.jpg']
    )
)

record_with_id = update_cid(cid_input, access_token='<your token here>')
print(json.dumps(record_with_id, indent=2))
```

**Assign Identifier**

```python
from cid_client import assign_identifier
import json
from cid_client.mapping_inputs import *


"""
    Assign a related CID, DOI, ARK or MARC identifier.
    Data is pulled from corresponding sources and saved as CID event. 
"""

assign_id_input = AssignIdentifierInput(
    cid='20.500.12592/ncjthz',
    identifier='10.1037/arc0000014',
    type=IdentifierTypeInput.DOI
)

updated_record = assign_identifier(assign_id_input, access_token='<your token here>')
print(json.dumps(updated_record, indent=2))
```

**Remove Identifier**

```python
from cid_client import remove_identifier
import json
from cid_client.mapping_inputs import *


"""
    Remove a related CID, DOI, ARK or MARC identifier.
"""

remove_id_input = RemoveIdentifierInput(
    cid='20.500.12592/ncjthz',
    identifier='10.1037/arc0000014',
    type=IdentifierTypeInput.DOI
)

updated_record = remove_identifier(remove_id_input, access_token='<your token here>')
print(json.dumps(updated_record, indent=2))
```

**Get by ID**

```python
from cid_client import get_by_id

"""
    Find CID if it exists.
    Returns full CID structure. 
"""

cid = get_by_id('20.500.12592/ncjthz')
print(cid)
```

**Get CID Children and Siblings**

```python
from cid_client import get_cid_children, get_cid_siblings


"""
    Find CID children and siblings.
    Returns list of matching CIDs and total.
    Result looks like this: {'total': 5, 'results': ['20.500.12592/ncjthz', ...]}
"""

search_res = get_cid_children('20.500.12592/fj6qk0')
print(search_res)

search_res = get_cid_siblings('20.500.12592/fj6qk0')
print(search_res)
```

**Get CID by artifact link**

```python
from cid_client import find_by_artifact


"""
    Find CID by artifact link.
    Returns list of matching CIDs and total. 
    Result looks like this: {'total': 5, 'results': ['20.500.12592/ncjthz']}
"""

search_res = find_by_artifact("https://www.osha.gov/Publications/OSHA3990.pdf")
print(search_res)
```

## Representation as IIIF format
You may notice that saved CID has a representation value like this: `https://3.17.81.42/iiif/95x6mc/manifest.json`

This is universal format described here: [https://iiif.io/](https://iiif.io/).

IIIF format allows you to easily generate image galleries by various UI plugins like this: 
[http://universalviewer.io](http://universalviewer.io)


## Thumbnails

There is a simple rule one can generate a thumbnail for CID. See example:

[https://3.17.81.42/ncjthz/300x300/thumbnail.png](https://3.17.81.42/ncjthz/300x300/thumbnail.png)

So, the format is:

```
    https://3.17.81.42/<CID_without_20.500.12592_fix>/<WIDTH>x<HEIGHT>/thumbnail.png
```