# HR_Media_Organizer
import sys, os, re
inputDir = '/home/justin/Desktop/testDir'

# Create an array of folders. 
files = os.chdir(inputDir)

# A function to prepare the folder name using our filters.
def cleanDir(string):
  # Define the dictionary of {'matches': 'replacements'}
  replacements = {'()': '', '[': '', ']': '', '{': '', '}': '', '.': ' ', '(': '', ')': '', 'BrRip': '', 'BRRip': '', 'XviD': '', 'BluRay':'', 'YIFY': '', '[YTS.AG]': '', '[YTS.PE]': '', 'HDTS': '', '720p': '', 'x264': '', 'AC3': '', '-': '', '1080p': '', ',': ''}
  # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
  # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
  # 'hey ABC' and not 'hey ABc'
  substrs = sorted(replacements, key=len, reverse=True)
  # Create a big OR regex that matches any of the substrings to replace
  regexp = re.compile('|'.join(map(re.escape, substrs)))
  # For each match, look up the new string in the replacements
  return regexp.sub(lambda match: replacements[match.group(0)], string)

# A function to prepare the filename using our filters.
def cleanFile(string):
  # Separate the last 4 characters (the file extension in the case of media, images, and subtitles which are all we need).
  stringExt = string[-4:]
  string = string[:-4]
  # Define the dictionary of {'matches': 'replacements'}
  replacements = {'()': '', '[': '', ']': '', '{': '', '}': '', '(': '', ')': '', 'BrRip': '', 'BRRip': '', 'XviD': '', 'BluRay':'', 'YIFY': '', '[YTS.AG]': '', '[YTS.PE]': '', 'HDTS': '', '720p': '', 'x264': '', 'AC3': '', '-': '', '1080p': '', '.': ' '}
  # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
  # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
  # 'hey ABC' and not 'hey ABc'.
  substrs = sorted(replacements, key=len, reverse=True)
  # Create a big OR regex that matches any of the substrings to replace.
  regexp = re.compile('|'.join(map(re.escape, substrs)))
  # For each match, look up the new string in the replacements and re-add the extension.
  return regexp.sub(lambda match: replacements[match.group(0)], string).rstrip(' ') + stringExt
# Verify that the target folder exists and is writable.
if os.access(inputDir, os.W_OK) is not True:
  print("inputDir not writable!")
  sys.exit()

# For each folder...
for dir in os.walk(inputDir):
  # Apply our filters to the input folder.
  oldDir = dir[0]
  newDir = cleanDir(oldDir)
  newDir = newDir.replace("   ", " ")
  newDir = newDir.replace("  ", " ")
  # Check if a folder already exists and create one if it does not.
  if os.path.exists(newDir) is not True:
    try:
      os.mkdir(newDir)
    except:
      print("newDir not writable!") 
  # Scan the folder for files.
  oldFiles = os.listdir(oldDir)
  # For each file within a folder...
  for oldFile in oldFiles:
    oldFilePath = os.path.join(oldDir, oldFile)
    # Make sure the file is real and not just a symlink.
    if (os.path.isfile(oldFilePath)):
      # Apply our filters to the input file.
      newFile = cleanFile(oldFile)
      print newFile
      newFilePath = newDir + '/' + newFile
      newFilePath = newFilePath.replace("   ", " ")
      newFilePath = newFilePath.replace("  ", " ")
      # Check that the target file doesn't already exist.
      if (os.path.isfile(newFilePath)):
        # Increment the filename if a file already exists with the same name.
        newFilePath = newDir + '/1_' + newFile
        os.rename(oldFilePath, newFilePath)
      if (os.path.isfile(newFilePath)) is not True:
        # Copy the file to the new directory.
        os.rename(oldFilePath, newFilePath)
  # After all files are processed try to delete the folder.
  # We could use shutil.rmtree instead but for this it's better to have errors with duplicates
  # that can be corrected instead of errors and deleted originals.
  if oldDir != newDir:
    try:
      os.rmdir(oldDir)
    except:
      print("Cannot Delete oldDir!")