import tempfile
import sys
import os
import subprocess

if len(sys.argv) < 2:
    print("USAGE: file_to_stdout.py <args>")
    exit(1)

out_file = tempfile.NamedTemporaryFile(prefix="out_").name

l_args = sys.argv[1:]
l_args.append(out_file)

p = subprocess.Popen(l_args, stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate()
if len(err) != 0 and not err.startswith("timelimit"):
    raise Exception(err)

print(output)
print(open(out_file, 'w').read())

if os.path.isfile(out_file):
    os.remove(out_file)
