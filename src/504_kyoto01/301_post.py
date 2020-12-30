import sys
sys.path.append('../500_common')
import lib
import lib_ss

# images = lib.get_images("../500_common/data/result.html")

soup = lib_ss.main("/Users/nakamurasatoru/git/d_genji/genji_curation/src/500_common/Chrome11", "Profile 1")
images = lib.get_images_by_soup(soup)

manifest = "https://kotenseki.nijl.ac.jp/biblio/100153620/manifest"
areas = ["3000,300,3000,4002", "145,300,3000,4002"]
countMax = 20

# token = lib.get_token("../token.yml")
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA4MGU0NWJlNGIzMTE4MzA5M2RhNzUyYmIyZGU5Y2RjYTNlNmU4ZTciLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoidS5uYWthbXVyYS5zYXRvcnUgdSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vLXBZeVhMVEpMeFE0L0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FDSGkzcmVWR21aMzNBQTRXSGloWGQ0aGZfSUcyNHpIX1EvcGhvdG8uanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NvZGgtODEwNDEiLCJhdWQiOiJjb2RoLTgxMDQxIiwiYXV0aF90aW1lIjoxNTk0MjQ4OTI2LCJ1c2VyX2lkIjoiUGwySXNUNWlVV1Z5SVZQUFFkNVNZbHZkdmV6MiIsInN1YiI6IlBsMklzVDVpVVdWeUlWUFBRZDVTWWx2ZHZlejIiLCJpYXQiOjE2MDkyOTE2MzcsImV4cCI6MTYwOTI5NTIzNywiZW1haWwiOiJ1Lm5ha2FtdXJhLnNhdG9ydUBnLmVjYy51LXRva3lvLmFjLmpwIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDExNzI0MzcwNTUzMjI0MjcwMDYiXSwiZW1haWwiOlsidS5uYWthbXVyYS5zYXRvcnVAZy5lY2MudS10b2t5by5hYy5qcCJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.oXP2ogG2JX1pLD2rpRs0V-PIrYDiOxqhyPbhKBmeSQ8vnS_a9-RZx16y-9I3k1vVQL1lHYIFMJre0VkOaP8sZhmrHFNm9xxAECf3GNkiGsd5lVGCtzhn6AJ4Iv3Sz6kIPggPyrb7vIk3RN2wnoIveT5ys4_kHM_h2pFQHRqPnRV91DD0G5ZU30S6MAOv-iACPqiuqpqrwKmU9TIB2_4kNimmLLiIB-_-LmkWLg7GYHmLQE1qLoRYj_GFX4EovajgW5QMdq_rLehjAGC-uBIOrasRKEqhO5F_igaJ_k0pgh2EyZr3OtGHhDY7zlAOq-VtaUH-7AlSNM7HNAO9ZM6KeA"

lib.post(manifest, areas, countMax, token, images, "Manifest")