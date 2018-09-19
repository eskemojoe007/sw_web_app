# SW Flight Searching Web App
This project is built on Django and Vue and is designed to search SW Flights.
pew jupyter-console

## Developer Notes

### WebPack Loader
These are production and other settings to host the proper static files through
Django.  Some people claim this is bad though.  So for now, I'll continue to host
both separately.  here are some of the resouces we could use however.

Webpack loader settings from http://v1k45.com/blog/modern-django-part-1-setting-up-django-and-react/
https://medium.com/@michealjroberts/part-1-integrating-django-2-vue-js-and-hot-webpack-reload-setup-387a975166d3
https://medium.com/@jrmybrcf/how-to-build-api-rest-project-with-django-vuejs-part-i-228cbed4ce0c

```python
WEBPACK_LOADER = {
 'DEFAULT': {
         'BUNDLE_DIR_NAME': '',
         'STATS_FILE': os.path.join(BASE_DIR, 'frontend', 'webpack-stats.dev.json'),
     }
}
```
