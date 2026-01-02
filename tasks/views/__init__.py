from .index_views import IndexView
from .auth_views import RegisterView, ActivateAccountView, ProfileView, ProfileUpdateView
from .worker_views import WorkerListView, WorkerDetailView
from .task_views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, toggle_task_status
from .task_type_views import TaskTypeListView, TaskTypeDetailView, TaskTypeCreateView, TaskTypeUpdateView, TaskTypeDeleteView, TaskTypeAnalyticsView
from .search_views import SearchView, search_suggest
from .avatar_views import AvatarChangeView
