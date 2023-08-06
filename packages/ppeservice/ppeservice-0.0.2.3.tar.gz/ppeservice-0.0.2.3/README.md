# py-production-experiment

This is an personal website generator (could be any website or small services generator). It control build, deploy, domain name generation and all process needed by having a website

### Testing curl command

* 

```bash
curl -d '{"username":"ttus", "password":"test"}' -X POST http://127.0.0.1:9888/login
```
* You can also test the APIs with Swagger UI by opening host:9888/api/docs

### Database Migration

1.  Choose the __config__ parameter from __./ppe/config/global_config.py__, the DevelopmentConfig will give you the ability of data migration

2. Change the data structure from the database_util/db.py

3. Run 

   ```bash
   ./ppeinstaller
   ```

4. Run

   ```bash
   ppe db init
   ```

4. Run 

   ```bash
   ppe db migrate
   ```

5. Run 

   ```bash
   ppe db upgrade
   ```

   to change the database to newer version (the data will not lost, but it'd better to have a backup)

   run 

   ```bash
   ppe db downgrade
   ```

   to revert to the old version

6. After everything above, do

   ```my
   drop table alembic_version
   ```

   and 

   ```bash
   rm migrations -rf
   ```

   