from pathlib import Path
import shutil

import labelbox
import requests
from PIL import Image
from tqdm import tqdm


def _make_dirs(dir='new_dir/'):
    """Create folders"""
    dir = Path(dir)
    if dir.exists():
        shutil.rmtree(dir)  # delete dir
    for p in dir, dir / 'labels', dir / 'images':
        p.mkdir(parents=True, exist_ok=True)  # make dir
    return dir


def _download_raw_content(api_key: str, proj_id: str):
    """Download labels and images url as json array

    Args:
        api_key (str): Labelbox API key
        proj_id (str): Labelbox Project ID

    Returns:
        raw_content (List): Raw content of labels and images as a json array
    """
    client = labelbox.Client(api_key)
    project = client.get_project(proj_id)
    raw_content = project.export_labels(
        download=True)  # json as list (json array)
    return raw_content


def download_images_and_labels(api_key: str, proj_id: str, out_path: Path):
    """ Download images and YOLO formated labels from Labelbox

    Args:
        api_key (str): Labelbox API key
        proj_id (str): Labelbox Project ID
        out_path (Path): Location to save images and labels
    """

    names = []  # class names
    save_dir = _make_dirs(out_path)

    # Download labels and images url as json array
    data = _download_raw_content(api_key, proj_id)

    for img in tqdm(data, desc=f'Downloading Images and Labels'):
        im_path = img['Labeled Data']
        im = Image.open(requests.get(im_path, stream=True).raw if im_path.startswith(
            'http') else im_path)  # open
        width, height = im.size  # image size
        label_path = save_dir / 'labels' / \
            Path(img['External ID']).with_suffix('.txt').name
        image_path = save_dir / 'images' / img['External ID']
        im.save(image_path, quality=95, subsampling=0)

        if 'objects' in img['Label']:
            for label in img['Label']['objects']:
                # box
                # top, left, height, width
                top, left, h, w = label['bbox'].values()
                xywh = [(left + w / 2) / width, (top + h / 2) / height,
                        w / width, h / height]  # xywh normalized

                # class
                cls = label['value']  # class name
                if cls not in names:
                    names.append(cls)

                # YOLO format (class_index, xywh)
                line = names.index(cls), *xywh
                with open(label_path, 'a') as f:
                    f.write(('%g ' * len(line)).rstrip() % line + '\n')

    print('Download completed successfully!')
    print(f'Found it at {save_dir}')


if __name__ == '__main__':
    api_key = ''
    proj_id = ''
    out_path = ''
    download_images_and_labels(api_key, proj_id, out_path)
