# crownstone-lib-python-cloud

Asynchronous Python library to get data from the cloud, and switch Crownstones.

## Functionality

* Async: using asyncio and aiohttp, optimized for speed.
* Easy to use: sync all your Crownstone Cloud data with just one command!
* Structurally sound: find your data with ease!
* Complete: set the switch state and brightness of your Crownstones remotely!

## Requirements

* Python 3.7 (only version that it's tested on currently)
* Aiohttp 3.6.2

## Standard installation

cd to the project folder and run:
```console
$ python3.7 setup.py install
```

## Install in a virtual environment

To install the library excute the following command:
```console
$ python3.7 -m venv venv3.7
```
Activate your venv using:
```console
$ source venv3.7/bin/activate
```
Once activated, the venv is used to executed python files, and libraries will be installed in the venv.<br>
To install this library, cd to the project folder and run:
```console
$ python setup.py install
```

## Getting started

### Examples

#### Async example

```Python
from crownstone_cloud.lib.cloud import CrownstoneCloud
import asyncio


async def main():
    # init cloud
    cloud = CrownstoneCloud('email', 'password')
    await cloud.initialize()

    # get a crownstone by name and switch it on
    crownstone = cloud.get_crownstone('awesomeCrownstone')
    await crownstone.turn_on()

    # switch all crownstones in a sphere to on:
    sphere = cloud.spheres.find('awesomeSphere')
    for crownstone in sphere.crownstones:
        await crownstone.turn_on()
    
    # close session
    # required when ran as standalone program, optional if ran in integration.
    await cloud.close_session()

asyncio.run(main())
```

#### Sync example

```Python
from crownstone_cloud.lib.cloud import CrownstoneCloud

# init cloud
cloud = CrownstoneCloud('email', 'password')
cloud.initialize_sync()

# get a crownstone and turn it on
crownstone = cloud.get_crownstone('awesomeCrownstone')
crownstone.turn_on_sync()

# close session
# required when ran as standalone program, optional if ran in integration.
cloud.close_session_sync()
```

### Initialization
Crownstone cloud is initialized with 2 arguments:
* User email
* User password

If you do not yet have a Crownstone account, go to [My Crownstone](https://my.crownstone.rocks) to set one up.
The email and password are used to re-login after an access token has expired.
```Python
cloud = CrownstoneCloud('email', 'password')
```
if already have an access token and you want to skip to first login for speed you can use:
```Python
cloud.set_access_token('myAccessToken')
```
to initialize all the cloud data into the lib, for async usage use:
```Python
await cloud.initialize()
```
Or for sync usage use:
```Python
cloud.initialize_sync()
```
It is only required to call initialize once at the beginning of the program.

## Data structure

The cloud can be displayed with the following structure:
* User
    * Keys
    * Spheres
        * Locations
        * Crownstones
        * Users
        

### User

The user is the to whom the data belongs.<br> 
The user is the one that logs in using email and password.<br>
By getting a user specific access token after login, the data for that specific user can be requested.

### Keys

The keys are user specific.<br> 
They are required to connect to the crownstone bluetooth mesh.<br>
The most common used keys are the sphere keys. They are located within each individual sphere.<br>

### Spheres

Spheres are the main data entry. They have rooms (locations), Crownstones and users in them.<br>
Example spheres:
* House
* Office
* Apartement

A Sphere has the following fields in the cloud lib:
* crownstones: Crownstones
* locations: Locations
* users: Users
* keys: Dict (optional, default = None)
* name: String
* cloud_id: String
* unique_id: String

### Locations

Locations are the rooms in your house or other building.<br>
For example for a house: 
* Livingroom
* Bedroom
* Garage
* Bathroom

A Location has the following fields in the cloud lib:
* present_people: List
* name: String
* cloud_id: String
* unique_id: String

### Crownstones

Crownstones are smart plugs that can make every device that isn't smart, way smarter!<br>
Crownstones are located within a sphere.<br>
Example names of Crownstones:
* Lamp
* Charger
* Television

A Crownstone has the following fields in the cloud lib:
* state: Float (0..1)
* dimming_enabled: Bool (default = False)
* name: String
* unique_id: String
* cloud_id: String
* type: String
* sw_version: String

### Users

Users are people who have access to a sphere.<br>
A user can have 3 roles:
* Admin
* Member
* Guest

A User has the following fields in the cloud lib:
* role: String
* first_name: String
* last_name: String
* email: String
* cloud_id: String
* email_verified: Bool

## Function list

### Cloud

#### initialize()
> Login if no access token available, and sync all data for the user from the cloud.

#### set_access_token(access_token: String)
> Set an access token to skip the login part, if you already have one

#### get_crownstone(crownstone_name: String) -> Crownstone
> Get a Crownstone object by name, if it exists.

#### get_crownstone_by_id(crownstone_id: String) -> Crownstone
> Get a Crownstone object by it's id, it's it exists.

### Spheres

#### update()
> Async function. Sync the Spheres with the cloud. Doing this will replace all current sphere data with that of the cloud.

#### find(sphere_name: String) -> Sphere
> Returns a sphere object if one exists by that name.

#### find_by_id(sphere_id: String) -> Sphere
> Return a sphere object if one exists by that id.

### Sphere

#### get_keys() -> Dict
> Async function. Returns a dict with the keys of this sphere. The keys can be used for BLE connectivity with the Crownstones.

### Crownstones

#### update()
> Async function. Sync the Crownstones with the cloud for a sphere. Doing this will replace all the current crownstone data with that of the cloud.

#### find(crownstone_name: String) -> Crownstone
> Return a Crownstone object if one exists by that name.

#### find_by_id(crownstone_id: String) -> Crownstone
> Return a Crownstone object if one exists by that id.

### Crownstone

#### turn_on()
> Async function. Send a command to turn a Crownstone on. To make this work make sure to be in the selected sphere and have Bluetooth enabled on your phone.

#### turn_off()
> Async function. Send a command to turn a Crownstone off. To make this work make sure to be in the selected sphere and have Bluetooth enabled on your phone.

#### set_brightness(percentage: Int)
> Async function. Send a command to set a Crownstone to a given brightness level. To make this work make sure to be in the selected sphere and have Bluetooth enabled on your phone.

### Locations

#### update()
> Async function. Sync the Locations en present people in that location with the cloud for a sphere. Doing this will replace all the current location data with that of the cloud.

#### find(location_name: String) -> Location
> Return a location object if one exists by that name.

#### find_by_id(location_id: String) -> Location
> Return a location object if one exists by that id.

### Users

#### update()
> Async function. Sync the Users with the cloud for a sphere. Doing this will replace all the current user data with that of the cloud.

#### find_by_first_name(first_name: String) -> List
> Returns a list of all users with that first name, as duplicate first names can exist.

#### find_by_last_name(last_name: String) -> List
> Return a list of all users with that last name, as duplicate last names can exist.

#### find_by_id(user_id: String) -> Location
> Return a location object if one exists by that id.

## Async vs sync
The lib can be used synchonously and asynchronously.<br>
Async functions need to be awaited:
```Python
await cloud.spheres.update()
```
All the async functions mentioned above can also be used synchronously.<br>
Simply type the same function name, but with underscore sync at the end. for example:
```Python
cloud.initialize_sync()
cloud.spheres.update_sync()
```
Make sure to see the examples above!

## Testing
To run the tests using tox install tox first by running:
```console
$ pip install tox
```
To execute the tests cd to the project folder and run:
```console
$ tox
```
To see which parts of the code are covered by the tests, a coverage report is generated after the tests have been successfull.<br>
To see the coverage report run:
```console
$ coverage report
```
If you like to get a better overview of the test you can generate a HTML file like so:
```console
$ coverage html
```
To view your html file directly on Linux:
```console
$ ./htmlcov/index.html
```
On Windows simply navigate to the htmlcov folder inside the project folder, and double-click index.html. It will be executed in your selected browser.
