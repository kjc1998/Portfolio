# Portfolio

## Progress

```
1) Public View Setup      [Done]
2) Personal Edit Setup    [Done]
3) Project Page           [Done]
4) Story Page             [Done]
5) Filter Bar             [0%]
6) UI                     [0%]
7) Cloud Hosting          [0%]
```

<br>

## Setting Up

1. Cloning repository and create .env file:

   ```shell
   git clone https://github.com/kjc1998/Portfolio.git
   cd Portfolio
   touch .env
   ```

2. Create entry for .env:

   ```shell
   DJANGO_SUPERUSER_USERNAME={USERNAME}
   DJANGO_SUPERUSER_PASSWORD={PASSWORD}
   DJANGO_SUPERUSER_EMAIL={EMAIL}
   ```

3. Setting up environment and installing dependencies:

   ```shell
   pip install virtualenv

   virtualenv portfolio           // can rename portfolio to any name
   source portfolio/bin/activate

   pip install -r requirement.txt // root directory
   ```

4. Setting up database:

   ```shell
   python portfolio/manage.py makemigrations
   python portfolio/manage.py migrate
   ```

5. Running application:

   ```shell
   source portfolio/bin/activate  // activate environment
   python portfolio/manage.py runserver
   ```

6. Setting django superuser:

   ```shell
   export $(cat .env | xargs)
   python portfolio/manage.py createsuperuser --noinput
   ```

<br>

## Links

<table>
   <tr>
      <th><b>URL</b></th>
      <th><b>Descriptions</b></th>
  </tr>

  <tr>
      <td>/main/</td>
      <td>
         <b>Home Page</b><br>
         Featuring projects, cv and contact details
      </td>
  </tr>

  <tr>
      <td>/admin/</td>
      <td>
         <b>Admin Page</b><br>
         Database overview
      </td>
  </tr>

  <tr>
      <td>/login/</td>
      <td>
         <b>Login Page</b><br>
         Login as superuser for edit functionalities
      </td>
  </tr>

  <tr>
      <td>/cv/</td>
      <td>
         <b>CV Management Page</b><br>
         Upload, Activate and Delete CV versions
      </td>
  </tr>

  <tr>
      <td>/project/</td>
      <td>
         <b>Project Listing</b><br>
         All projects that have been added to portfolio
      </td>
  </tr>

  <tr>
      <td>/project/pid/</td>
      <td>
         <b>Story Listing</b><br>
         Depicting all stories under this project in reverse chronological order
      </td>
  </tr>

  <tr>
      <td>/project/pid/sid/</td>
      <td>
         <b>Story Page</b><br>
         Detailed event/contributions to the project (short story, image, and skill tags)
      </td>
  </tr>
</table>

<br>

## Settings & Development

**Notes:**

_Details concerning code development & adjustments to personal preferences_

_Changes to UI and In-placed images_

<br>

[Individual Media Changes](https://github.com/kjc1998/Portfolio/tree/master/portfolio/media) (for simple changes only with the same template)

[BackEnd Code Stucture](https://github.com/kjc1998/Portfolio/tree/master/portfolio)

[FrontEnd Code Stucture](https://github.com/kjc1998/Portfolio/tree/master/portfolio/templates)
