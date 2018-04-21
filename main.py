import flickrapi
import os
import cv2
import urllib
from pathlib import Path
import json
import csv

api_key = os.environ['FLICKR_KEY']
api_secret = os.environ['FLICKR_SECRET']

filtered_photos = []

flickr=flickrapi.FlickrAPI(api_key,api_secret,cache=True)

path_to_saved_images = './'

# def save_tagger_csv(keyword, url_list):
#     csv_name = path_to_saved_images + keyword+'/'+keyword+'_url_info.csv'
#     with open(csv_name, 'wb') as csvfile:
#         csv_writer = csv.writer(csvfile, delimiter=',')
#         csv_writer.writerow(['image_url'])
#         for url in url_list:
#             csv_writer.writerow([url])


# def save_photo_info(keyword, all_photos_information):
#     file_name = path_to_saved_images+keyword+'/'+keyword + '_photos_info.json'
#     with open(file_name, 'w') as f:
#         json.dump(all_photos_information, f)


def flickr_walk(keyword, num_results):
    all_photos_information = {}
    all_urls = []

    extras = 'url_c,url_m,description,license,owner_name'
    photos = flickr.walk(text=keyword,
                         tag_mode='all',
                         tags=keyword,
                         extras=extras,
                         per_page=500,
                         sort='relevance')

    for i, photo in enumerate(photos):
        if int(photo.get('license')) > 1:
            filtered_photos.append(photo)
            if len(filtered_photos) >= num_results:
                break
    counter = 0
    download_counter = 0
    for photo in filtered_photos:
        counter +=1
        image_name = photo.get('url_m')
        saved_image_name = image_name.split('https://')[1].split('.staticflickr.com/')[1].split('/')[1]
        folder_name = '/'+keyword+'/'
        path_to_saved_image = path_to_saved_images+folder_name+saved_image_name
        if not Path(path_to_saved_image).is_file(): 
            download_success = True
            try:
                urllib.urlretrieve(image_name, path_to_saved_image)
            except Exception as e:
                print e
                download_success = False
            if download_success == True:
                download_counter +=1
                print download_counter
                photo_info = {
                    'name': image_name,
                    'license': photo.get('license'),
                    'owner': photo.get('ownername'),
                    'owner_id': photo.get('owner'),
                    'title': photo.get('title'),
                    'url': photo.get('url_m')
                }
                all_photos_information[saved_image_name] = photo_info
                all_urls.append(photo.get('url_m'))
        else:
            print 'file exists: ',Path(path_to_saved_image)
    # save_photo_info(keyword, all_photos_information)
    # save_tagger_csv(keyword, all_urls)

flickr_walk('cat', 5)
