# CEPy Resources
This will be the hub for Resources relating to creating `CEPy` (Core Environment: Python) extensions using my project, [PyShiftAE](https://github.com/Trentonom0r3/PyShiftAE).
Using `PyShiftAE`, I hope to provide users a way to create extensions entirely using python, hence `CEPy`. 

This is even more of a work in progress than `PyShiftAE`. 

## Contents
- [Example-Ideas](#example-ideas)
- [API-Reference](https://github.com/Trentonom0r3/PyShiftAE/wiki/API-Reference)
    - [CSXS Events](https://github.com/Trentonom0r3/PyShiftAE/wiki/CSXS-Utils)
    - [Demos](https://github.com/Trentonom0r3/PyShiftAE/wiki/Demos)
    - [Building from source](https://github.com/Trentonom0r3/PyShiftAE/wiki/Building-from-source)
    - [Pre-Compiled .aex Binary](https://github.com/Trentonom0r3/PyShiftAE/blob/main/dist/PyShiftAE.aex)
      - MUST have Python 3.11 installed to path.
  
- [Contributing](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md)
    - [Issues](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#reporting-issues)
    - [Pull Requests](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#submitting-pull-requests)
    - [Guidelines](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#code-guidelines)
    - [Testing](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#testing)
    - [Docs](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#docs)
    - [Community](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#community-interaction)
    - [Legal](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#legal)
    - [Setup](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#environment-setup)
    - [Review Process](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#review-process)
    - [Acknowledgements](https://github.com/Trentonom0r3/PyShiftAE/blob/main/CONTRIBUTING.md#acknowledgements)
      - All contributors will be acknowledged in the project repository. Your contributions, no matter how small, are valuable to us and the community.

## Usage 
- To Create a `CEP` Extension that uses Python as opposed to extendscript, there are a few steps you must take.
  - First, Ensure you have the latest version of ```PyShiftAE``` installed, and python 3.11 on your system's path.
  - Secondly, clone this repo, and run ```build.py```.
    - ```build.py``` will walk you through setting up your extension's Manifest, and then generate your initial structure. This structure (and the file names) should not be changed, but the contents/details can be. 
- At this point, you have a directory set up containing ```manifest.py```, ```entry.py```, and ```PyShiftCore.pyi```
  - If you need to make any changes to your manifest (such as new dependencies), add them there.
    - ```entry.py``` is where you define all of your functions for use. It is recommended NOT to use global variables here. Instead, use ```entry.py``` as your function definition "bridge". For utilities, I recommend separating into a different file, then importing into ```entry.py```. It keeps things clean, and makes debugging easier for you. The boilerplate code created for you contains comments detailing structure and format you should try and maintain, as well as points where you shouldn't really mess with things.
    - in `entry.py`, you can import from other scripts within the same directory. However, if those other scripts also have local imports, you must add the lines;
      ```py
      script_dir = os.path.dirname(__file__)  # Path to the directory where your script is located
      sys.path.append(script_dir)  # Add this directory to the Python path
      ```
    - So that your files may be properly imported.
         
    - Provided as part of ```PyShiftAE```, is a built-in debug console. All python stdout and stderr is redirected to this window, when open. Find it under ```Window``` -> ```Python Console```. Read Only. 
    
- Provided all previous steps were completed successfully, you are now set up to integrate python with your CEP extension. 
  - To do this, utilize the ```PyInterface.ts``` file from this repo in your CEP extension.
    - Add your `comp.psc.EXTENSIONNAME` folder into your CEP folder, and make sure it is placed at the common CEP location: `C:\Program Files (x86)\Common Files\Adobe\CEP\extensions` 
      - ```PyInterface``` will communicate with ```PyShiftAE``` as necessary, and will return results to the user as strings.
        - (It is up to the user to convert to numbers, etc, as needed).
         - ```PyInterface```  uses a structure that will seem somewhat familiar to users of ```CSInterface.js.```
           - Example Usage:
                ```js
                const callpy = async () =>{
                    const pyi = new PyInterface('ABCD'); //Create the PyInterface using your Manifest.Name.
                    await pyi.connect(); //Connect to the plugin.

                    // Sync call
                    const result = await pyi.evalPy('say_hello'); //Follows the signature pyi.evalPy('FUNCTIONNAME', arg1, arg2, arg3,...)
                    console.log(result);
                }
                ```

        - I Highly recommend using BOLT-CEP for development, as it will streamline the process. 
