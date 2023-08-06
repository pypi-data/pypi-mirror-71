# djangocms-opensystem

A plugin for Django CMS that displays OpenSystem widgets.

## Installation

1. Install module using pipenv:
  ```
  pipenv install djangocms-opensystem
  ```

  *Or pip:*
  
  ```
  pip install djangocms-opensystem
  ```

2. Add it to your installed apps:
  ```
  "djangocms_opensystem",
  ```

3. Apply migrations
  ```
  python manage.py migrate djangocms_opensystem
  ```

4. Include your BASKET_ID and INTEGRATION_ID in your settings
  ```python
  DJANGOCMS_OPENSYSTEM_BASKET_ID = "<your basket ID>"
  DJANGOCMS_OPENSYSTEM_INTEGRATION_ID = <your integration ID>
  ```

5. Make sure to have a sekizai’s `{% render_block "bottom_js" %}` in your base template