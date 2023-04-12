volumes:
  - ./docker/mysql/scripts:/docker-entrypoint-initdb.d
  - ./mysql_data:/var/lib/mysql