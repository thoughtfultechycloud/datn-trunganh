import io
import shutil
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import path

from .models import Backup, Restore

SQLITE_MAGIC = b'SQLite format 3\x00'
BACKUP_DIR = Path(settings.BASE_DIR) / 'backups'


def _list_backups():
    if not BACKUP_DIR.exists():
        return []
    files = sorted(BACKUP_DIR.glob('*.bak'), key=lambda f: f.stat().st_mtime, reverse=True)
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
            db_path = settings.DATABASES['default']['NAME']
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'backup_{timestamp}.bak'
            dest = BACKUP_DIR / filename
            shutil.copy2(db_path, dest)

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
        filename = Path(filename).name  # chống path traversal
        filepath = BACKUP_DIR / filename
        if not filepath.exists() or filepath.suffix != '.bak':
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
            if not content.startswith(SQLITE_MAGIC):
                return JsonResponse({'error': 'File không hợp lệ — không phải SQLite database.'}, status=400)

            db_path = settings.DATABASES['default']['NAME']
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            shutil.copy2(db_path, str(db_path) + f'.before_restore_{timestamp}')

            with open(db_path, 'wb') as f:
                f.write(content)

            return JsonResponse({'ok': True})

        context = self.admin_site.each_context(request)
        context['title'] = 'Khôi phục dữ liệu'
        return render(request, 'admin/restore.html', context)
