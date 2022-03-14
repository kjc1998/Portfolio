# Portfolio

## Progress:

- Public View Setup [Done]
- Personal Edit Setup [Done]
- Project Page [Done]
- Story Page [Done]
- Filter Bar [0%]
- UI [0%]
- Google Cloud Hosting [0%]

<br>

## Setting Up:

create .env at root folder (Portfolio)

1. cloning repository and create .env file:

   ```shell
   git clone https://github.com/kjc1998/Portfolio.git
   cd Portfolio
   touch .env
   ```

2. create entry for .env:

   ```shell
   USERNAME={USERNAME}
   PASSWORD={PASSWORD}
   EMAIL={EMAIL}
   ```

3. setting up environment and installing dependencies:

   ```shell
   pip install virtualenv

   virtualenv portfolio           // can rename portfolio to any name
   source portfolio/bin/activate

   pip install -r requirement.txt // root directory
   ```

4. running application:

   ```shell
   source portfolio/bin/activate  // activate environment
   python portfolio/manage.py runserver
   ```

5. setting django superuser:

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
         Home page for this application<br>
         Featuring projects, cv and contact details
      </td>
  </tr>

  <tr>
      <td>/cv/</td>
      <td>
         CV management page<br>
         Upload, Activate and Delete CV versions
      </td>
  </tr>

  <tr>
      <td>/project/</td>
      <td>
         Project listing<br>
         All projects that have been added to portfolio
      </td>
  </tr>

  <tr>
      <td>/project/pid/</td>
      <td>
         Story listing<br>
         Depicting all stories under this project in reverse chronological order
      </td>
  </tr>

  <tr>
      <td>/project/pid/sid/</td>
      <td>
         Story details<br>
         Detailed event/contributions to the project (short story, image, and skill tags)
      </td>
  </tr>
</table>
