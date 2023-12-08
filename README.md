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

## Example Ideas
- Within PyShiftCore:
  ```python
    class Manifest:
    #list valid version of AE. Technically it is AE2016, AE2017, AE2018, AE2019, AE2020, AE2021, AE2022, AE2023, and up, but
    # we need a simpler way to convey that
    AE_MIN = 2000 # DO NOT CHANGE
    AE_MAX = 3000 # DO NOT CHANGE
    PYTHON_DEFAULT = "3.11" # DO NOT CHANGE
    PATH = os.path.dirname(os.path.realpath(__file__))
    def __init__(self, name = None, version = None, author = None,
                 description = None, AE_VERS = None, PY_VERS = None, 
                 main = None, ui = None, resources = None, dependencies = None, extras = None):
        
        # Basic Information
        self.name = "YourPluginName"
        self.version = "1.0.0"
        self.author = "Your Name"
        self.description = "Brief description of what your plugin does."
        self.size = (300, 300) # Size of the UI window. Default is (300, 300)
        self.resizable = True # Whether the UI window is resizable. Default is False
        # Compatibility Information
        self.AE_VERS = ["AE2021", "AE2022"] #Default, will automatically define range of AE versions, not require to define
                                            # by user, unlike CEP manifests.
        self.PY_VERS = self.PYTHON_DEFAULT  # Default, unless you built PyShiftCore from source. 

        # Path Information, relative to the manifest file
        self.main = "path/to/main_script.py"  # Path to the main Python script
        self.ui = "path/to/ui_script.py"      # Path to the UI Python script. If None, no UI will be loaded.
        self.resources = "path/to/resources"  # Folder for additional resources

        # Dependencies
        self.dependencies = ["numpy", "opencv-python"]  # List of required Python libraries
        self.extras = ["path/to/additional/file1", "path/to/additional/file2"]

        # Advanced Settings           
        self.cache = True  # Indicate the user will be caching data, so the manifest will know to create a cache folder
        self.cache_path = "path/to/cache"  # Path to the cache folder. Where the manifest will create the cache
        self.cache_size = 100  # Size of the cache in MB. Default is 100MB
        self.cache_max = 1000  # Maximum size of the cache in MB. Default is 1000MB
        self.cache_clear_when_full = True  # Clear the cache when it is full. Default is True

    # You can add methods to validate, load, or process the manifest information
    def _validate_versions(self):
        # Validate AE versions
        for version in self.AE_VERS:
            if not self.AE_MIN <= int(version[2:]) <= self.AE_MAX:
                raise ValueError("Invalid AE version: {}".format(version))

        # Validate Python version
        if not self.PY_VERS.startswith("3."):
            raise ValueError("Invalid Python version: {}".format(self.PY_VERS))

    def _validate_paths(self):
        #validate PATH
        if not os.path.exists(self.PATH):
            raise ValueError("Invalid path to manifest: {}".format(self.PATH))
        
        if not os.path.exists(self.main):
            raise ValueError("Invalid path to main script: {}".format(self.main))
        
        if self.ui is not None and not os.path.exists(self.ui):
            raise ValueError("Invalid path to UI script: {}".format(self.ui))
        
        if not os.path.exists(self.resources):
            raise ValueError("Invalid path to resources: {}".format(self.resources))
        
        for extra in self.extras:
            if not os.path.exists(extra):
                raise ValueError("Invalid path to extra file: {}".format(extra))
            
            
    def _validate_dependencies(self):
        #validate dependencies
        for dependency in self.dependencies:
            try:
                __import__(dependency)
            except ImportError:
                raise ValueError("Missing dependency: {}".format(dependency))
            
    def validate(self):
        self._validate_versions()
        self._validate_paths()
        self._validate_dependencies()
        return True
    
    def load(self):
        if self.ui is not None:
            # Extract the filename without the extension
            ui_module_name = os.path.splitext(os.path.basename(self.ui))[0]
            main_module_name = os.path.splitext(os.path.basename(self.main))[0]

            # Load and import the ui module
            spec = importlib.util.spec_from_file_location(ui_module_name, self.ui)
            ui_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ui_module)

            # Load and import the main module
            spec = importlib.util.spec_from_file_location(main_module_name, self.main)
            main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
                
        pass
    
  class Entry:
      def __init__(self, manifest: Manifest):
          self.manifest = manifest
          self.cache = Cache(manifest.cache_path)
  
       
  class Cache:
      def __init__(self, path):
          self.path = path
          self.min_size = 100
          self.max_size = 1000
          self.clear_when_full = True

    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    def __getattr__(self, name):
        return self.__dict__[name]
   ```
  
- From the User side:
   ```python
   class TKEntry(Entry):
      def __init__(self, manifest: Manifest):
          super().__init__(manifest)
          self.root = Tk()
          self.root.title(manifest.name)
          self.root.geometry("{}x{}".format(manifest.size[0], manifest.size[1]))
          self.root.resizable(manifest.resizable, manifest.resizable)
          # add slider
          # add buttons
          self.buttons = []
          self.sliders = []
          
      def add_button(self, name, command):
          button = tkinter.Button(self.root, text=name, command=command)
          button.pack()
          self.buttons.append(button)
          
      def add_slider(self, name, min, max, default):
          slider = tkinter.Scale(self.root, from_=min, to=max, orient=tkinter.HORIZONTAL)
          slider.pack()
          self.sliders.append(slider)
          
      #create a text entry
      def add_text(self, name):
          text = tkinter.Entry(self.root)
          text.pack()
          self.texts.append(text)
          
      def get_text(self, name):
          for text in self.texts:
              if text.cget("text") == name:
                  return text.get()
                  break
          return None
      
      def set_slider(self, name, value):
          for slider in self.sliders:
              if slider.cget("text") == name:
                  slider.set(value)
                  break
      
      def run(self):
          self.root.mainloop()

  if __name__ == "__main__":
      def overLOAD():
          print("overload") # create a function to overload the cache.load function
        
      cache = Cache("path/to/cache")
      cache.load = lambda: overLOAD() # create a new attribute to the cache object
      cache.save = lambda: print("saving cache") # create a new attribute to the cache object
      cache.test = "test" # create a new attribute to the cache object
      
      manifest = Manifest() # create a manifest object
      manifest.cache = True # set the cache attribute to True
      manifest.cache_path = "path/to/cache" # set the cache path
      manifest.cache_size = 100 # set the cache size
      manifest.cache_max = 1000 # set the cache max
      manifest.cache_clear_when_full = True   # set the cache clear when full
      
      def add_new_text(text):  # create a function to add a new text entry
          entry.add_text(text)
          
      entry = TKEntry(manifest) # create a TKEntry object
      entry.add_button("test", add_new_text(entry.get_text("test"))) # add a button to the UI
      entry.add_slider("test", 0, 100, 50) # add a slider to the UI
      entry.add_text("test") # add a text entry to the UI
      entry.run() # run the UI
    ```
