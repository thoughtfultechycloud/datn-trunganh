import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import path

from .models import Backup, Restore

PGDUMP_MAGIC = b'PGDMP'
BACKUP_DIR = Path(settings.BASE_DIR) / 'backups'


def _db_env():
    db = settings.DATABASES['default']
    return {
        **os.environ,
        'PGPASSWORD': db.get('PASSWORD', ''),
    }


def _db_args():
    db = settings.DATABASES['default']
    return [
        '-h', db.get('HOST', 'localhost'),
        '-p', str(db.get('PORT', '5432')),
        '-U', db.get('USER', 'postgres'),
        '-d', db.get('NAME', 'postgres'),
    ]


def _list_backups():
    if not BACKUP_DIR.exists():
        return []
    files = sorted(BACKUP_DIR.glob('*.dump'), key=lambda f: f.stat().st_mtime, reverse=True)
    result = []
    for f in files:
        stat = f.stat()
        size_kb = round(stat.st_size / 1024, 1)
        result.append({
            'name': f.name,
            'size': f'{size_kb} KB',
            'mtime': datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M:%S'),
        })
    return result


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):

    def get_urls(self):
        return [
            path(
                '',
                self.admin_site.admin_view(self.backup_page),
                name='backup_backup_changelist',
            ),
            path(
                'download/<str:filename>/',
                self.admin_site.admin_view(self.download_backup),
                name='backup_download',
            ),
        ]

    def backup_page(self, request):
        if request.method == 'POST':
            BACKUP_DIR.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'backup_{timestamp}.dump'
            dest = BACKUP_DIR / filename

            try:
                subprocess.run(
                    ['pg_dump', '-Fc', '-f', str(dest)] + _db_args(),
                    env=_db_env(),
                    check=True,
                    capture_output=True,
                )
            except FileNotFoundError:
                return JsonResponse(
                    {'error': 'Không tìm thấy pg_dump. Hãy cài postgresql-client hoặc rebuild Docker image.'},
                    status=500,
                )
            except subprocess.CalledProcessError as e:
                return JsonResponse(
                    {'error': f'pg_dump thất bại: {e.stderr.decode(errors="replace")}'},
                    status=500,
                )

            content = dest.read_bytes()
            response = HttpResponse(content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(content)
            return response

        context = self.admin_site.each_context(request)
        context['title'] = 'Sao lưu dữ liệu'
        context['backups'] = _list_backups()
        return render(request, 'admin/backup.html', context)

    def download_backup(self, request, filename):
        filename = Path(filename).name
        filepath = BACKUP_DIR / filename
        if not filepath.exists() or filepath.suffix != '.dump':
            raise Http404
        content = filepath.read_bytes()
        response = HttpResponse(content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(content)
        return response


@admin.register(Restore)
class RestoreAdmin(admin.ModelAdmin):

    def get_urls(self):
        return [
            path(
                '',
                self.admin_site.admin_view(self.restore_page),
                name='backup_restore_changelist',
            ),
        ]

    def restore_page(self, request):
        if request.method == 'POST':
            uploaded = request.FILES.get('backup_file')
            if not uploaded:
                return JsonResponse({'error': 'Không tìm thấy file.'}, status=400)

            content = uploaded.read()
            if not content.startswith(PGDUMP_MAGIC):
                return JsonResponse(
                    {'error': 'File không hợp lệ — không phải pg_dump custom format.'},
                    status=400,
                )

            # Auto-backup trước khi khôi phục
            BACKUP_DIR.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            auto_dest = BACKUP_DIR / f'auto_before_restore_{timestamp}.dump'
            try:
                subprocess.run(
                    ['pg_dump', '-Fc', '-f', str(auto_dest)] + _db_args(),
                    env=_db_env(),
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                pass  # không chặn restore nếu auto-backup thất bại

            with tempfile.NamedTemporaryFile(suffix='.dump', delete=False) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                subprocess.run(
                    ['pg_restore', '--clean', '--if-exists', '-Fc'] + _db_args() + [tmp_path],
                    env=_db_env(),
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                return JsonResponse(
                    {'error': f'pg_restore thất bại: {e.stderr.decode(errors="replace")}'},
                    status=500,
                )
            finally:
                os.unlink(tmp_path)

            return JsonResponse({'ok': True})

        context = self.admin_site.each_context(request)
        context['title'] = 'Khôi phục dữ liệu'
        return render(request, 'admin/restore.html', context)
