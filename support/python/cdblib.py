def create (file_name):
  import json, io, os, errno

  try:
      os.remove(file_name)                # delete the file if it exsists
      with open(file_name, 'w'): pass     # create an empty file
  except OSError as e:
      if e.errno == errno.ENOENT:         # errno.ENOENT = no such file or directory
         with open(file_name, 'w'): pass  # create an empty file
      else:
          raise                           # report an exception

  # Create and save an empty dict
  data_out = {}
  with io.open(os.getcwd() + '/' + file_name, 'w', encoding='utf-8') as out_file:
      out_file.write(json.dumps(data_out,
                                indent=2,
                                sort_keys=True,
                                separators=(',', ': '),
                                ensure_ascii=False)+'\n')

# put and get based on ~/Python/examples/dict-io/lcb-01.py

def put (key_name,object,file_name):
  import json, io, os
  import cadabra2
  __cdbkernel__ = cadabra2.__cdbkernel__

  # Read the current dict
  with io.open(os.getcwd() + '/' + file_name) as inp_file:
      data_out = json.load(inp_file)

  # Add a new entry to the dict.

  # Two choices here. Both give almost identical output except for the rule symbol '->'.
  # Using str(object) will write this using unicode characters. This causes problems
  # down the track -- when these rules are imported in other codes we get a Python
  # error -- it reports that it can't handle this unicode character.
  # Using object.input_form() does the trick. It writes out '->'. This is good.

  # data_out[key_name] = str(object)       # will write rule char using unicode
  data_out[key_name] = object.input_form() # will write rule char as '->'

  # Save the updated dict
  with io.open(os.getcwd() + '/' + file_name, 'w', encoding='utf-8') as out_file:
      out_file.write(json.dumps(data_out,
                                indent=2,
                                sort_keys=True,
                                separators=(',', ': '),
                                ensure_ascii=False)+'\n')

def get (key_name,file_name):
  import json, io, os
  import cadabra2
  __cdbkernel__ = cadabra2.__cdbkernel__

  # Read the current dict
  with io.open(os.getcwd() + '/' + file_name) as inp_file:
      data_inp = json.load(inp_file)

  # Return one entry from the dict
  return cadabra2.Ex (data_inp[key_name])
