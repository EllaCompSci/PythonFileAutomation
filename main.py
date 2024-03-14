import os
import pathlib

import pathlib as pathlib
import shutil
import time
from os.path import exists

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

downloadFolder = pathlib.Path.home() / "Downloads"
text_folder = "//smbhome.uscs.susx.ac.uk/cb792/Documents/Downloaded Text"
dsa_folder = "//smbhome.uscs.susx.ac.uk/cb792/Documents/Downloaded Text/dsa"
fp_folder = "//smbhome.uscs.susx.ac.uk/cb792/Documents/Downloaded Text/fp"
ics_folder = "//smbhome.uscs.susx.ac.uk/cb792/Documents/Downloaded Text/ics"
image_folder = "//smbhome.uscs.susx.ac.uk/cb792/Documents/Downloaded Images"

if not exists(text_folder):
    os.mkdir(text_folder)
if not exists(dsa_folder):
    os.mkdir(dsa_folder)
if not exists(fp_folder):
    os.mkdir(fp_folder)
if not exists(ics_folder):
    os.mkdir(ics_folder)
if not exists(image_folder):
    os.mkdir(image_folder)

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


    def on_created(event):
        if event.src_path.endswith('.txt'):
            try:
                os.remove(event.src_path)
                shutil.copy(event.src_path, text_folder)
            except EnvironmentError:
                return

        if event.src_path.endswith('.pdf'):

            if event.src_path.startswith('DSA2024'):
                try:
                    shutil.copy(event.src_path, dsa_folder)
                    os.remove(event.src_path)
                except EnvironmentError:
                    return
            elif event.src_path.startswith('FP'):
                try:
                    shutil.copy(event.src_path, fp_folder)
                    os.remove(event.src_path)
                except EnvironmentError:
                    return
            elif event.src_path.startswith('ICS'):
                try:
                    shutil.copy(event.src_path, ics_folder)
                    os.remove(event.src_path)
                except EnvironmentError:
                    return
            else:
                try:
                    shutil.copy(event.src_path, text_folder)
                    os.remove(event.src_path)

                except EnvironmentError:
                    return

        if event.src_path.endswith('.png') or event.src_path.endswith('.jpg'):
            try:
                shutil.copy(event.src_path, image_folder)
                os.remove(event.src_path)
            except EnvironmentError:
                return


    def on_modified(event):
        if event.src_path.endswith('.txt'):
            try:
                os.remove(event.src_path)
                shutil.copy(event.src_path, text_folder)
            except EnvironmentError:
                return

        if event.src_path.endswith('.pdf'):
            if "DSA" in event.src_path:
                try:
                    shutil.copy(event.src_path, dsa_folder)
                    os.remove(event.src_path)
                except EnvironmentError:
                    return
            elif "FP" in event.src_path:
                try:
                    shutil.copy(event.src_path, fp_folder)
                    os.remove(event.src_path)
                except EnvironmentError:
                    return
            elif "ICS" in event.src_path:
                try:
                    shutil.copy(event.src_path, ics_folder)
                    os.remove(event.src_path)
                except EnvironmentError:
                    return
            else:
                try:
                    shutil.copy(event.src_path, text_folder)
                    os.remove(event.src_path)

                except EnvironmentError:
                    return
        if event.src_path.endswith('.png') or event.src_path.endswith('.jpg'):
            try:
                shutil.copy(event.src_path, image_folder)
                os.remove(event.src_path)
            except EnvironmentError:
                return


    my_event_handler.on_created = on_created
    my_event_handler.on_modified = on_modified

    path = downloadFolder
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
