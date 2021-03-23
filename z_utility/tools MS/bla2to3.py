import os
import 2to3
your_directory = r'M:\Music Software\mackie c4 pro c4c_pc_v1.0\makeLIVE_APIsource-archive\mlostekk-live\branches\old_working\accessories\originalSources\API_MakeDoc\_Support'
for dirpath, b, filenames in os.walk(your_directory):
    for filename in filenames:
        if not filename.endswith('.pyc'):
            continue

        filepath = dirpath + '/' + filename
        original_filename = filename.split('.')[0]
        original_filepath = dirpath + '/' + original_filename + '.py'
        with open(original_filepath, 'w') as f:
            uncompyle6.decompile_file(filepath, f)