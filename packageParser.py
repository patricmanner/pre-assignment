import os
import re


def parse_packages():
    packages = {}
    currentPackage = ''

    if os.path.exists('/var/lib/dpkg/status.real'):
        filePath = '/var/lib/dpkg/status.real'

    else:
        filePath = 'status.real'
    file = open(filePath, 'r', encoding='utf-8')

    for line in file:  # Loop file line by line

        if line.startswith('Package:'):  # Get package name
            currentPackage = line[8:].strip()

            if not currentPackage in packages:  # Might have been initialized through a reverse dependency. If not, do it here
                packages[currentPackage] = {}

        elif line.startswith('Description:'):  # Get package description
            packages[currentPackage]['description'] = line.rstrip() + '.'

        elif line.startswith(' ') and \
            'description' in packages[currentPackage] and \
                re.search('[a-zA-Z]', line):  # Descriptions are usually folded fields, so get the whole description by
                                              # finding lines that starts with whitespace. If line contains actual text,
                                              # concatenate it to description, otherwise the line signifies an empty line
                packages[currentPackage]['description'] = packages[currentPackage]['description'] + line.rstrip()

        elif line.startswith('Depends:'):  # Get dependencies
            dependencies = re.split(': |, |\\|', line)
            dependencies.pop(0)  # Remove the first 'Depends:' item
            noVerDependencies = []

            for dependency in dependencies:  # Loop through dependencies and remove version as well as add reverse
                                             # dependencies to their package details
                index = dependency.find(' ')

                if index > -1:  # Found version, remove it
                    dependency = dependency[0:index]
                noVerDependencies.append(dependency)

                if dependency not in packages:  # Add reverse dependency (create the dependency's dict if needed)
                    packages[dependency] = {}

                if 'reverseDependency' not in packages[dependency]:
                    packages[dependency]['reverseDependency'] = [currentPackage]

                else:
                    packages[dependency]['reverseDependency'].append(currentPackage)
            packages[currentPackage]['depends'] = noVerDependencies
    file.close()
    return packages
