# Repository naming
To get information of how this user is naming the repositories go [here](https://github.com/DysonParra#repository-naming)

# Information of the project.
  Cli lib that receive an undetermined number of arguments, analyze if are correctly formed and if yes parse it into objects or else print the specific error in console.    
The flags are from two types (you can use the two at same time):  
  * With value: an alphanumeric string started with '-' and the next argument must be the value of the flag.  
  Example:  -downloadPath documents   -sourceFile myFile.xml   -rootDir C:/project  
  * Withouth value: an alphanumerirc string started with '--'.  
  Example:  --useDefault  --notUseIncognito  --generateLogFile  --preserveTempFiles  

    For use the library you need to specify in source code a sets of flags:
    * Required: The flags that if are not included in the arguments the lib return an error.  
    * Optional: The flags that can or not be included in the arguments withouth problem.  
    * Default: The flags that are used if the cli arguments not specify any flag.  

The required and the optional flags are a matrix (can be different size), that in each row defined a set of flags that are just like a XOR, only one of these flags must be included, and the default flags are a vector, example:

    required = [ "-name"  "--notUseName"           ]    optional = [ "-loadPageTimeOut"                ]
               [ "-chromeDriverPath"               ]               [ "-outputPath" "-notGenerateFiles" ]
               [ "-account"  "--notLogin" "-token" ]                                                     
    
    default = [ "-name"  "dev"  "-chromeDriverPath"  "/opt/driver"  "--notLogin"  "-outputPath"  "/out"]

In the example:  
  - One and only one of the flags "-name" and "--notUseName" must be included.  
  - The flag "-chromeDriverPath" must be included.  
  - One and only one of the flags "-account", "--notLogin" and "-token" must be included.  
  - The flag "-loadPageTimeOut" can be or not included.  
  - Can include one of the flags "-outputPath" or "-notGenerateFiles", but not the two.
  - If the cli argument list is void the default flags are used, so the default flags must be defined in such way that all required flags are specified.

The lib also validate that a flag is not defined as required and as optional at same time.  
For use the library use as example the code in "Application.py" (the main class), the escense of the code is call the method "convert_args_to_flags" and if not return null the flags are OK, else in the console you can see exactly which is the error.
