import os
import re


def parse_packages():
    packages = {}
    currentPackage = ''
    realFile = True

    if os.path.exists('/var/lib/dpkg/status'):
        filePath = '/var/lib/dpkg/status'

    else:
        filePath = 'status.real'
        realFile = False
    file = open(filePath, 'r', encoding='utf-8')

    for line in file:  # Loop file line by line

        if line.startswith('Package:'):  # Get package name
            currentPackage = line[8:].strip()
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
            dependencies = re.split(': |, | \\| ', line)
            dependencies.pop(0)  # Remove the first 'Depends:' item
            noVerDependencies = []

            for dependency in dependencies:  # Loop through dependencies and remove version
                index = dependency.find(' ')

                if index > -1:  # Found version, remove it
                    dependency = dependency[0:index]
                noVerDependencies.append(dependency.rstrip())
            packages[currentPackage]['depends'] = noVerDependencies
    file.close()

    for package in packages:  # loop through packages and add reverse dependencies

        if 'depends' in packages[package].keys():

            for depends in packages[package]['depends']:

                if depends in packages.keys():

                    if 'reverseDependency' not in packages[depends]:
                        packages[depends]['reverseDependency'] = [package]

                    else:
                        packages[depends]['reverseDependency'].append(package)
    return packages, realFile
