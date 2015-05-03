#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pkg_resources


def get_pkg_license(pkgname):
    """
    Given a package reference (as from requirements.txt),
    return license listed in package metadata.
    NOTE: This function does no error checking and is for
    demonstration purposes only.
    """
    pkgs = pkg_resources.require(pkgname)
    pkg = pkgs[0]

    try:
        for line in pkg.get_metadata_lines('PKG-INFO'):
            (k, v) = line.split(': ', 1)
            if k == "License":
                return v

    except Exception:
        return None

    return None


def clean_license_string(lic):
    lic = lic.lower()
    lic = lic.replace("license", "")
    lic = lic.replace("version", "")
    lic = lic.replace(",", "")
    lic = lic.strip()
    lic = ' '.join(lic.split())
    lic = lic.upper()
    return lic


def main():
    licenses = {}
    for pkg in pkg_resources.working_set:
        lic = get_pkg_license(pkg.project_name)
        if lic:
            lic = clean_license_string(lic)

        lic_list = licenses.get(lic)
        if lic_list is not None:
            lic_list.append(pkg.project_name)
            licenses[str(lic)] = lic_list
        else:
            licenses[str(lic)] = [pkg.project_name]


    print json.dumps(licenses, indent=2)


if __name__ == '__main__':
    main()

