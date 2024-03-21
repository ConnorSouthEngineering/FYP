import os
import fnmatch
import random
import shutil
from datetime import datetime
import requests

def find_classes_and_non_matching(parent_path, class_names):
    
    class_directories = {class_name: [] for class_name in class_names}
    class_directories["Other"] = []  
    for item in os.listdir(parent_path):
        item_path = os.path.join(parent_path, item)
        if os.path.isdir(item_path):
            
            matched = False
            for class_name in class_names:
                if item.lower().startswith(class_name.lower()):
                    class_directories[class_name].append(item_path)
                    matched = True
                    break
            if not matched:
                
                class_directories["Other"].append(item_path)
    return class_directories

def find_directories(sources, directory_path, classes):
    class_paths = {"Other": []}  
    for class_name in classes:  
        class_paths[class_name] = []
    for source in sources:
        source_path = os.path.join(directory_path, source)
        print(f"Processing source path: {source_path}")
        if os.path.exists(source_path):
            
            found_directories = find_classes_and_non_matching(source_path, classes)
            
            for key, paths in found_directories.items():
                class_paths[key].extend(paths)

    return class_paths


def find_files(class_paths):
    class_files = {}
    for class_type in class_paths:
        directories = class_paths[class_type]
        for directory in directories:
            files = fnmatch.filter(os.listdir(directory), "*.mp4")
            if files:  
                if class_type not in class_files:
                    class_files[class_type] = {}
                class_files[class_type][directory] = files
    return class_files

def display_tree(class_files):
        for class_type, directories in class_files.items():
            print(f"Class: {class_type}")
            for directory, files in directories.items():
                print(f"  ├─ Directory: {directory}")
                displayed_files = files[:10]
                for file in displayed_files[:-1]:
                    print(f"  │   ├─ {file}")
                if displayed_files:
                    if len(files) > 10:
                        print(f"  │   ├─ {displayed_files[-1]}")
                        print(f"  │   └─ ... (and {len(files) - 10} more files)")
                    else:
                        print(f"  │   └─ {displayed_files[-1]}")
            print() 

def adjust_count(class_directories, training_amount):
    reduced_class_files = {}
    for class_name, directories in class_directories.items():
        reduced_class_files[class_name] = {}
        required_vid_count = training_amount
        initial_dir_count = training_amount // len(directories)
        total_vid_count = sum(len(os.listdir(dir_path)) for dir_path in directories)
        if total_vid_count < training_amount:
            print(f"Warning: Not enough videos for class {class_name}. Available: {total_vid_count}, Needed: {training_amount}")
            required_vid_count = total_vid_count
        for dir_path in directories:
            available_videos = os.listdir(dir_path)  
            needed_videos = min(len(available_videos), initial_dir_count if required_vid_count >= initial_dir_count else required_vid_count)
            selected_videos = random.sample(available_videos, needed_videos)
            reduced_class_files[class_name][dir_path] = selected_videos
            required_vid_count -= needed_videos
            remaining_directories = len(directories) - len(reduced_class_files[class_name])
            if remaining_directories > 0:
                initial_dir_count = required_vid_count // remaining_directories
    return reduced_class_files

def copy_files(final_files, splits, model_name):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    base_dir = f"../model_tasks/{model_name}_{timestamp}"
    os.makedirs(base_dir, exist_ok=True)
    
    split_dirs = {split: os.path.join(base_dir, split) for split in splits.keys()}
    for split_dir in split_dirs.values():
        os.makedirs(split_dir, exist_ok=True)

    for class_name, directories in final_files.items():
        all_files = []
        for directory, filenames in directories.items():
            for filename in filenames:
                all_files.append(os.path.join(directory, filename))

        random.shuffle(all_files)

        for split, count in splits.items():
            split_dir = split_dirs[split]
            
            class_dir = os.path.join(split_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
            
            split_files = all_files[:count]
            all_files = all_files[count:]  
            
            for file_path in split_files:
                dest_path = os.path.join(class_dir, os.path.basename(file_path))
                shutil.copy(file_path, dest_path)
                print(f"Copied {file_path} to {dest_path}")
    return base_dir

def get_model_parmeters(task_id):
    try:
        classes_result = requests.get(f"http://localhost:3000/tasks/{task_id}/classes")
        sources_result = requests.get(f"http://localhost:3000/tasks/{task_id}/sources")
        task_result = requests.get(f"http://localhost:3000/tasks/{task_id}")
        classes = classes_result.json()[0]['get_task_classes']["classes"]
        sources = sources_result.json()[0]['get_task_sources']["sources"]
        task = task_result.json()[0]['get_task'][0]
        splits = {"train": task['train'], "validation":task['verification'], "test":task['test']}
        model_name = task['model_name']
        return classes, sources, splits, model_name
    except:
        print("Change status to failed")

def get_class_maps(classes):
    class_result = requests.get(f"http://localhost:3000/maps/class")
    class_map = class_result.json()[0]['get_class_map']
    class_names = []
    for class_id in classes:
        class_names.append(class_map[f"{class_id}"])
    return class_names

def get_source_maps(sources):
    source_result = requests.get(f"http://localhost:3000/maps/source")
    source_map = source_result.json()[0]['get_source_map']
    source_names = []
    for source_id in sources:
        source_names.append(source_map[f"{source_id}"])
    return source_names

async def pull_files(task_id):
    classes, sources, splits, model_name = get_model_parmeters(task_id)
    classes = get_class_maps(classes)
    sources = get_source_maps(sources)
    directory_path = "./sources"
    class_paths = find_directories(sources, directory_path, classes)
    class_files = find_files(class_paths)
    display_tree(class_files)
    final_files = adjust_count(class_files,sum(splits.values()))
    display_tree(final_files)
    base_dir = copy_files(final_files,splits,model_name)
    print(f"Files Moved to {base_dir}")
    return base_dir  