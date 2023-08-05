import argparse
import csv
import glob
import json
import os
import re
import time

from math import ceil
from shutil import copyfile, rmtree
from urllib.parse import urlparse
from pyproc import Lpse, __version__, utils
from pyproc.helpers import DetilDownloader
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime


EXIT_CODE = 0


def print_info():
    print(r'''    ____        ____                 
   / __ \__  __/ __ \_________  _____
  / /_/ / / / / /_/ / ___/ __ \/ ___/
 / ____/ /_/ / ____/ /  / /_/ / /__  
/_/    \__, /_/   /_/   \____/\___/  
      /____/                        
SPSE4 Downloader, PyProc v{}
'''.format(__version__))

def set_last_downloaded_rows(index_path, rows):
    with open(os.path.join(os.path.dirname(index_path), 'index.meta'), 'w') as f:
        f.write(str(rows))

def get_last_downloaded_rows(index_path):
    if not os.path.isfile(index_path) or not index_path.endswith('lock'):
        return 0

    metadata = os.path.join(os.path.dirname(index_path), 'index.meta')
    metadata_line = 0
    file_line = 0

    try:
        with open(metadata, 'r') as f:
            metadata_line = int(f.read().strip())
    except:
        pass

    with open(index_path, 'r') as f:
        for file_line, _ in enumerate(f):
            pass
        file_line += 1

    if metadata_line == file_line:
        return metadata_line

    return 0

def download_index(lpse, fetch_size, timeout, non_tender, index_path, index_path_exists, force, delay):
    lpse.timeout = timeout

    print("url SPSE       :", lpse.host)
    print("versi SPSE     :", lpse.version)
    print("last update    :", lpse.last_update)
    print("\nIndexing Data")

    if index_path_exists and not force:
        yield "- Menggunakan cache"
    else:
        if non_tender:
            total_data = lpse.get_paket_non_tender()['recordsTotal']
        else:
            total_data = lpse.get_paket_tender()['recordsTotal']

        batch_size = int(ceil(total_data / fetch_size))
        last_downloaded_rows = get_last_downloaded_rows(index_path)
        downloaded_row = last_downloaded_rows if last_downloaded_rows > 0 else 0
        temp_downloaded_row = 0
        mode = 'a' if last_downloaded_rows > 0 else 'w'

        with open(index_path, mode, newline='', encoding='utf8',
                  errors="ignore") as index_file:

            writer = csv.writer(index_file, delimiter='|', quoting=csv.QUOTE_ALL)

            for page in range(batch_size):

                temp_downloaded_row += fetch_size

                if temp_downloaded_row <= last_downloaded_rows:
                    pass
                else:
                    if non_tender:
                        data = lpse.get_paket_non_tender(start=page*fetch_size, length=fetch_size, data_only=True)
                        min_data = list(map(lambda x: [x[0], x[6]], data))
                    else:
                        data = lpse.get_paket_tender(start=page*fetch_size, length=fetch_size, data_only=True)
                        min_data = list(map(lambda x: [x[0], x[8]], data))

                    writer.writerows(min_data)
                    downloaded_row += len(min_data)
                    set_last_downloaded_rows(index_path, downloaded_row)

                    time.sleep(delay)

                yield [page+1, batch_size, downloaded_row]


def get_detil(downloader, jenis_paket, tahun_anggaran, index_path):
    detail_dir = os.path.join(get_folder_name(downloader.lpse.host, jenis_paket), 'detil')

    os.makedirs(detail_dir, exist_ok=True)

    downloader.download_dir = detail_dir
    downloader.error_log = detail_dir+".err"
    downloader.is_tender = True if jenis_paket == 'tender' else False

    with open(index_path, 'r', encoding='utf8', errors="ignore") as f:
        reader = csv.reader(f, delimiter='|')

        for row in reader:
            tahun_anggaran_data = re.findall(r'(20\d{2})', row[1])

            if not download_by_ta(tahun_anggaran_data, tahun_anggaran):
                continue

            downloader.queue.put(row[0])

    downloader.queue.join()



def combine_data(host, jenis_paket, remove=True, filename=None, tahun_anggaran=None):
    '''
    Combine data detil LPSE hasil download.
    :param host: host LPSE
    :param jenis_paket: tender atau pengadaan langsung
    :param remove: remove data detil setelah di-merge
    :param filename: nama file hasil merge data
    :param tahun_anggaran: filter tahun anggaran. fungsi filter tahun anggaran di fungsi ini hanya untuk data yang
                           tidak memiliki tahun anggaran, sehingga filter akan dilakukan atas tanggal pembuatan
                           paket
    :return:
    '''
    folder_name = get_folder_name(host, jenis_paket=jenis_paket)
    detil_dir = os.path.join(folder_name, 'detil', '*')
    detil_combined = os.path.join(folder_name, 'detil.dat')
    detil_all = glob.glob(detil_dir)
    detil_all.sort()

    pengumuman_nontender_keys = {
        'id_paket': None,
        'kode_paket': None,
        'nama_paket': None,
        'tanggal_pembuatan': None,
        'keterangan': None,
        'tahap_paket_saat_ini': None,
        'instansi': None,
        'satuan_kerja': None,
        'kategori': None,
        'metode_pengadaan': None,
        'tahun_anggaran': None,
        'nilai_pagu_paket': None,
        'nilai_hps_paket': None,
        'lokasi_pekerjaan': None,
        'npwp': None,
        'nama_peserta': None,
        'penawaran': None,
        'penawaran_terkoreksi': None,
        'hasil_negosiasi': None,
        'p': False,
        'pk': False,
        'v': False
    }

    pengumuman_keys = {
        'id_paket': None,
        'kode_tender': None,
        'nama_tender': None,
        'tanggal_pembuatan': None,
        'keterangan': None,
        'tahap_tender_saat_ini': None,
        'instansi': None,
        'satuan_kerja': None,
        'kategori': None,
        'sistem_pengadaan': None,
        'tahun_anggaran': None,
        'nilai_pagu_paket': None,
        'nilai_hps_paket': None,
        'lokasi_pekerjaan': None,
        'npwp': None,
        'nama_peserta': None,
        'penawaran': None,
        'penawaran_terkoreksi': None,
        'hasil_negosiasi': None,
        'p': False,
        'pk': False,
        'v': False
    }

    with open(detil_combined, 'w', encoding='utf8', errors="ignore", newline='') as csvf:
        fieldnames = list(pengumuman_keys.keys() if jenis_paket == 'tender' else pengumuman_nontender_keys.keys())
        fieldnames += ['penetapan_pemenang_mulai', 'penetapan_pemenang_sampai', 'penandatanganan_kontrak_mulai',
                       'penandatanganan_kontrak_sampai']

        writer = csv.DictWriter(
            csvf,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for detil_file in detil_all:
            detil = pengumuman_keys.copy() if jenis_paket == 'tender' else pengumuman_nontender_keys.copy()

            detil.update(
                {
                    'penetapan_pemenang_mulai': None,
                    'penetapan_pemenang_sampai': None,
                }
            )

            with open(detil_file, 'r', encoding='utf8', errors="ignore") as f:
                data = json.loads(f.read())

            tahun_pembuatan = re.findall(r'(20\d{2})', data['pengumuman']['tanggal_pembuatan'])
            has_tahun_anggaran = re.findall(r'(20\d{2})', data['pengumuman']['tahun_anggaran'])

            if not has_tahun_anggaran and not download_by_ta(tahun_pembuatan, tahun_anggaran):
                continue

            detil['id_paket'] = data['id_paket']

            if data['pengumuman']:
                detil.update((k, data['pengumuman'][k]) for k in detil.keys() & data['pengumuman'].keys())

                detil['lokasi_pekerjaan'] = ' || '.join(detil['lokasi_pekerjaan'])

                if jenis_paket == 'tender':
                    tahap = 'tahap_tender_saat_ini'
                else:
                    tahap = 'tahap_paket_saat_ini'

                if detil[tahap]:
                    detil[tahap] = detil[tahap].strip(r' [...]')

            if data['jadwal']:
                data_pemenang = list(filter(lambda x: x['tahap'] == 'Penetapan Pemenang', data['jadwal']))
                data_kontrak = list(filter(lambda x: x['tahap'] == 'Penandatanganan Kontrak', data['jadwal']))

                if data_pemenang:
                    detil['penetapan_pemenang_mulai'] = data_pemenang[0]['mulai']
                    detil['penetapan_pemenang_sampai'] = data_pemenang[0]['sampai']

                if data_kontrak:
                    detil['penandatanganan_kontrak_mulai'] = data_kontrak[0]['mulai']
                    detil['penandatanganan_kontrak_sampai'] = data_kontrak[0]['sampai']

            if data['hasil']:
                pemenang = utils.get_pemenang_from_hasil_evaluasi(data['hasil'])

                if not pemenang and jenis_paket == 'non_tender':
                    pemenang = data['hasil'][0:]

                if pemenang is not None and len(pemenang) > 0:
                    detil.update((k, pemenang[0][k]) for k in detil.keys() & pemenang[0].keys())

            writer.writerow(detil)

            del detil

    copy_result(folder_name, remove=remove, filename=filename)


def error_writer(error, update_exit_code=True):
    global EXIT_CODE

    if update_exit_code:
        EXIT_CODE = 1
    with open('error.log', 'a', encoding='utf8', errors="ignore") as error_file:
        error_file.write(error+'\n')


def get_folder_name(host, jenis_paket):
    _url = urlparse(host)
    netloc = _url.netloc if _url.netloc != '' else _url.path

    return netloc.lower().replace('.', '_') + '_' + jenis_paket


def get_index_path(cache_folder, host, jenis_paket, last_paket_id):
    index_dir = os.path.join(cache_folder, get_folder_name(host, jenis_paket))

    os.makedirs(index_dir, exist_ok=True)

    index_path = os.path.join(index_dir, 'index-{}-{}-{}'.format(*last_paket_id))

    return os.path.isfile(index_path), index_path


def parse_tahun_anggaran(tahun_anggaran):
    parsed_ta = tahun_anggaran.strip().split('-')
    error = False

    for i in range(len(parsed_ta)):
        try:
            parsed_ta[i] = int(parsed_ta[i])
        except ValueError:
            parsed_ta[i] = 0

    if len(parsed_ta) > 2:
        error = True
    elif parsed_ta[-1] == 0:
        parsed_ta[-1] = 9999

    return error, parsed_ta


def download_by_ta(ta_data, ta_argumen):

    if not ta_data:
        return True

    ta_data = [int(i) for i in ta_data]

    for i in ta_data:
        if ta_argumen[0] <= i <= ta_argumen[-1]:
            return True

    return False


def copy_result(folder_name, remove=True, filename=None):

    if filename is None:
        filename = folder_name
    else:
        filename = ''.join(filename.split('.')[:-1])

    copyfile(os.path.join(folder_name, 'detil.dat'), filename + '.csv')

    if os.path.isfile(os.path.join(folder_name, 'detil.err')):
        copyfile(os.path.join(folder_name, 'detil.err'), filename + '_error.log')

    if remove:
        rmtree(folder_name)


def get_last_paket_id(lpse: Lpse, tender=True):
    # first
    if tender:
        data_first = lpse.get_paket_tender(start=0, length=1)
        data_last = lpse.get_paket_tender(start=0, length=1, ascending=True)
    else:
        data_first = lpse.get_paket_non_tender(start=0, length=1)
        data_last = lpse.get_paket_non_tender(start=0, length=1, ascending=True)

    if data_first and data_last:
        if not data_first['recordsTotal'] == 0:
            return [data_first['data'][0][0], data_last['data'][0][0], data_first['recordsTotal']]

    return None


def create_cache_folder():
    from pathlib import Path

    home = str(Path.home())
    cache_folder = os.path.join(home, '.pyproc')

    os.makedirs(cache_folder, exist_ok=True)

    return cache_folder


def lock_index(index_path):
    return index_path+".lock"


def unlock_index(index_path):
    unlocked_path = index_path.split(".lock")[0]
    os.rename(index_path, unlocked_path)

    return unlocked_path


def main():
    print_info()
    cache_folder = create_cache_folder()
    disable_warnings(InsecureRequestWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Alamat Website LPSE", default=None, type=str)
    parser.add_argument("--out", help="Nama file hasil download LPSE", default=None, type=str)
    parser.add_argument("-r", "--read", help="Membaca host dari file", default=None, type=str)
    parser.add_argument("--tahun-anggaran", help="Tahun Anggaran untuk di download", default=str(datetime.now().year),
                        type=str)
    parser.add_argument("--workers", help="Jumlah worker untuk download detil paket", default=8, type=int)
    parser.add_argument("--fetch-size", help="Jumlah row yang didownload per halaman", default=100, type=int)
    parser.add_argument("--timeout", help="Set timeout", default=30, type=int)
    parser.add_argument("--keep", help="Tidak menghapus folder cache", action="store_true")
    parser.add_argument("--index-download-delay", help="Menambahkan delay untuk setiap iterasi halaman index",
                        default=1, type=int)
    parser.add_argument("--non-tender", help="Download paket non tender (penunjukkan langsung)", action="store_true")
    parser.add_argument("--force", "-f", help="Clear index sebelum mendownload data", action="store_true")
    parser.add_argument("--skip-spse-check", help="skip cek versi SPSE", action="store_true")

    args = parser.parse_args()

    error, tahun_anggaran = parse_tahun_anggaran(args.tahun_anggaran)
    jenis_paket = 'non_tender' if args.non_tender else 'tender'

    if error:
        print("ERROR: format tahun anggaran tidak dikenal ", args.tahun_anggaran)
        exit(1)

    if args.host:
        host_list = args.host.strip().split(',')
    elif args.read:
        with open(args.read, 'r', encoding='utf8', errors="ignore") as host_file:
            host_list = host_file.read().strip().split()
    else:
        parser.print_help()
        print("\nERROR: Argumen --host atau --read tidak ditemukan!")
        exit(1)

    # download index
    detil_downloader = DetilDownloader(workers=args.workers, timeout=args.timeout, use_cache=not args.force)
    detil_downloader.spawn_worker()

    try:
        for host in host_list:
            _ = host.split(';')
            host = _[0].strip()
            custom_file_name = None

            if args.host and args.out:
                custom_file_name = args.out.strip()
            elif len(_) > 1:
                custom_file_name = _[1].strip()

            try:
                print("=" * len(host))
                print(host)
                print("=" * len(host))
                print("tahun anggaran :", ' - '.join(map(str, tahun_anggaran)))
                print("jenis paket    :", 'Pengadaan Langsung' if args.non_tender else 'Tender')
                _lpse = Lpse(host=host, timeout=args.timeout, skip_spse_check=args.skip_spse_check)
                last_paket_id = get_last_paket_id(_lpse, not args.non_tender)

                if last_paket_id is None:
                    print("- Data kosong")
                    continue

                index_path_exists, index_path = get_index_path(cache_folder, _lpse.host, jenis_paket, last_paket_id)

                if args.force:
                    rmtree(os.path.dirname(index_path))
                    os.mkdir(os.path.dirname(index_path))
                    index_path_exists = False

                if not index_path_exists:
                    index_path = lock_index(index_path)

                for downloadinfo in download_index(_lpse, args.fetch_size, args.timeout, args.non_tender, index_path,
                                                   index_path_exists, args.force, args.index_download_delay):
                    if index_path_exists and not args.force:
                        print(downloadinfo, end='\r')
                        continue

                    print("- halaman {} of {} ({} row)".format(*downloadinfo), end='\r')

                print("\n- download selesai\n")

                index_path = unlock_index(index_path)

            except Exception as e:
                print("ERROR:", str(e))
                error_writer('{}|{}'.format(host, str(e)))
                continue

            print("Downloading")

            detil_downloader.reset()
            detil_downloader.set_host(lpse=_lpse)

            get_detil(downloader=detil_downloader, jenis_paket=jenis_paket, tahun_anggaran=tahun_anggaran,
                      index_path=index_path)
            print("\n- download selesai\n")

            print("Menggabungkan Data")
            try:
                combine_data(_lpse.host, jenis_paket, not args.keep, filename=custom_file_name,
                             tahun_anggaran=tahun_anggaran)
            except Exception as e:
                print("ERROR:", str(e))
                error_writer('{}|menggabungkan {}'.format(host, str(e)))
            print("- proses selesai")

    except KeyboardInterrupt:
        error = "\n\nProses dibatalkan oleh user, bye!"
        print(error)
        error_writer("{}|{}".format(detil_downloader.lpse.host, error))
        detil_downloader.stop_process()
    except Exception as e:
        print("\n\nERROR:", e)
        error_writer("{}|{}".format(detil_downloader.lpse.host, str(e)))
        detil_downloader.stop_process()
    finally:
        for i in range(detil_downloader.workers):
            detil_downloader.queue.put(None)

        for t in detil_downloader.threads_pool:
            t.join()


if __name__ == '__main__':
    main()
    exit(EXIT_CODE)
