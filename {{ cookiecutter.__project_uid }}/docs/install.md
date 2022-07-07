# Install

In this chapter, I explain how to install the project and its dependencies in order to run it on your computer.

## Install Python

The project has been tested with *Python 3.8* to *Python 3.10*. To ensure the best compatibility, I recommend using version *3.8*. Here are the instructions on how to install it on your computer.

### On Windows

```{eval-rst}
.. warning::
   *Python 3.8* is not compatible with *Windows XP* or earlier.
```

1. Download the installer ([64-bit](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe) / [32-bit](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)).
2. Run the downloaded installer.
3. Make sure you check both **Install launcher for all users (recommended)** and **Add *Python 3.8* to PATH**.
4. Click on **Install now**. This will install Python using the recommended method, including *pip* and *IDLE*.
5. Click on **Disable path length limit**. This allows *Python* to use long path names.

*Python 3.8* is now installed on your machine.

### On MacOS

1. Download the installer ([Intel](https://www.python.org/ftp/python/3.8.10/python-3.8.10-macosx10.9.pkg) / [Apple Silicon](https://www.python.org/ftp/python/3.8.10/python-3.8.10-macos11.pkg)).
2. Run the downloaded installer.
3. Click **Continue** and use the default settings.

*Python 3.8* is now installed on your machine.

### On Linux

*Python 3.8* is available as a package for most of the *Linux* distributions. Use your package manager to install it using pre-built binaries.

```{eval-rst}
.. warning::
   On some distributions, *pip* and *venv* are not included in the same package as *Python*. Make sure to install them in order to use the project.
```

## Install the project

The first step is to extract the project in a directory where you want to install it.

I recommend using a virtual environment to run the project. This brings several benefits:

- It prevents dependency hell.
- It emproves reproducibility.
- It allows you to reinstall the project from scratch if needed (or when upgrading).

To create a virtual environment, follow these intructions.

### On Windows

1. Open *Power Shell* in the directory of the project.
2. ```
   python38 -m venv .venv
   ```
3. Activate the virtual environement.  
   ```
   .\.venv\Scripts\activate
   ```
4. Install the project and its dependencies.  
   ```
   python3 -m pip install .
   ```

### On MacOS

1. Open a terminal in the directory of the project.
2. Use the following command.  
   ```
   python3.8 -m venv .venv
   ```
3. Activate the virtual environement.  
   ```
   source .venv/bin/activate
   ```
4. Install the project and its dependencies.  
   ```
   python3 -m pip install .
   ```

### On Linux

1. Open a terminal in the directory of the project.
2. Use the following command.  
   ```
   python3.8 -m venv .venv
   ```
3. Activate the virtual environement.  
   ```
   source .venv/bin/activate
   ```
4. Install the project and its dependencies.  
   ```
   python3 -m pip install .
   ```