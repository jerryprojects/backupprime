import React, { useState } from 'react';
import { Login } from './components/Login';
import { Dashboard } from './components/Dashboard';
import { ProjectDetail } from './components/ProjectDetail';
import { ProjectCreation } from './components/ProjectCreation';
import { Profile } from './components/Profile';
import { Landing } from './components/Landing';
import { AdminDashboard } from './components/AdminDashboard';
import { Settings } from './components/Settings';
import { defaultLandingContent, LandingContent } from './data/landingContent';

export type UserRole = 'student' | 'faculty' | 'admin';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
}

export type ProjectStatus = 'public' | 'locked' | 'approved';

export interface TeamMember {
  name: string;
  email: string;
  contribution: string;
}

export interface Project {
  id: string;
  title: string;
  abstract: string;
  domains: string[];
  year: string;
  license: string;
  techStack: string[];
  status: ProjectStatus;
  owner: string;
  ownerId: string;
  teamMembers: TeamMember[];
  createdAt: string;
  lastUpdated: string;
  approvedFacultyIds?: string[]; // Track which faculty members have been granted access
  approvalStatus?: 'pending' | 'approved' | 'rejected'; // Admin approval status
}

export interface AccessRequest {
  id: string;
  projectId: string;
  facultyId: string;
  facultyName: string;
  status: 'pending' | 'approved' | 'rejected';
  timestamp: string;
}

export type ViewType = 'dashboard' | 'project-detail' | 'create-project' | 'profile' | 'settings';

function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [currentView, setCurrentView] = useState<ViewType>('dashboard');
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [accessRequests, setAccessRequests] = useState<AccessRequest[]>([]);
  const [showLogin, setShowLogin] = useState(false);
  const [landingContent, setLandingContent] = useState<LandingContent>(defaultLandingContent);
  const [allUsers, setAllUsers] = useState<User[]>([]);
  const [isAuthChecking, setIsAuthChecking] = useState(true);

  // Check if user is already authenticated on mount
  React.useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('authToken');
      if (token) {
        try {
          const response = await fetch('http://localhost:8000/api/users/me/', {
            headers: { 'Authorization': `Token ${token}` },
          });
          
          if (response.ok) {
            const userProfile = await response.json();
            const user: User = {
              id: String(userProfile.id),
              email: userProfile.email,
              name: userProfile.first_name && userProfile.last_name 
                ? `${userProfile.first_name} ${userProfile.last_name}`
                : userProfile.username,
              role: userProfile.profile?.role || 'student',
            };
            setCurrentUser(user);
            setCurrentView('dashboard');
          } else {
            // Token invalid, clear it
            localStorage.removeItem('authToken');
          }
        } catch (err) {
          console.error('Auth check error:', err);
          localStorage.removeItem('authToken');
        }
      }
      setIsAuthChecking(false);
    };

    checkAuth();
  }, []);

  const handleLogin = (user: User) => {
    setCurrentUser(user);
    setCurrentView('dashboard');
    setShowLogin(false);
    // Add user to users list if not already present
    if (!allUsers.find(u => u.email === user.email)) {
      setAllUsers([...allUsers, user]);
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setCurrentView('dashboard');
    localStorage.removeItem('authToken');
    setShowLogin(false);
  };

  const handleNavigate = (view: ViewType, projectId?: string) => {
    setCurrentView(view);
    if (projectId) {
      setSelectedProjectId(projectId);
    }
  };

  const handleCreateProject = (project: Project) => {
    setProjects([...projects, { ...project, approvalStatus: 'pending' }]);
    setCurrentView('dashboard');
  };

  const handleRequestAccess = (projectId: string) => {
    if (!currentUser) return;
    
    const newRequest: AccessRequest = {
      id: `req-${Date.now()}`,
      projectId,
      facultyId: currentUser.id,
      facultyName: currentUser.name,
      status: 'pending',
      timestamp: new Date().toISOString(),
    };
    
    setAccessRequests([...accessRequests, newRequest]);
  };

  const handleApproveRequest = (requestId: string) => {
    setAccessRequests(
      accessRequests.map(req =>
        req.id === requestId ? { ...req, status: 'approved' as const } : req
      )
    );

    const request = accessRequests.find(req => req.id === requestId);
    if (request) {
      setProjects(
        projects.map(proj =>
          proj.id === request.projectId
            ? { 
                ...proj, 
                approvedFacultyIds: [...(proj.approvedFacultyIds || []), request.facultyId]
              }
            : proj
        )
      );
    }
  };

  const handleRejectRequest = (requestId: string) => {
    setAccessRequests(
      accessRequests.map(req =>
        req.id === requestId ? { ...req, status: 'rejected' as const } : req
      )
    );
  };

  const handleApproveProject = (projectId: string) => {
    setProjects(
      projects.map(proj =>
        proj.id === projectId ? { ...proj, approvalStatus: 'approved' as const } : proj
      )
    );
  };

  const handleRejectProject = (projectId: string) => {
    setProjects(
      projects.map(proj =>
        proj.id === projectId ? { ...proj, approvalStatus: 'rejected' as const } : proj
      )
    );
  };

  // Show loading while checking authentication
  if (isAuthChecking) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-500 rounded-2xl mb-4 animate-pulse">
            <div className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">PRIME</h1>
          <p className="text-slate-300">Loading...</p>
        </div>
      </div>
    );
  }

  if (!currentUser) {
    if (!showLogin) {
      return <Landing onGetStarted={() => setShowLogin(true)} content={landingContent} />;
    }
    return <Login onLogin={handleLogin} onBack={() => setShowLogin(false)} />;
  }

  // Admin view
  if (currentUser.role === 'admin') {
    return (
      <AdminDashboard
        user={currentUser}
        landingContent={landingContent}
        onUpdateContent={setLandingContent}
        onLogout={handleLogout}
      />
    );
  }

  const selectedProject = selectedProjectId
    ? projects.find(p => p.id === selectedProjectId)
    : null;

  return (
    <div className="min-h-screen bg-slate-50">
      {currentView === 'dashboard' && (
        <Dashboard
          user={currentUser}
          projects={projects}
          setProjects={setProjects}
          accessRequests={accessRequests}
          onNavigate={handleNavigate}
          onLogout={handleLogout}
          onApproveRequest={handleApproveRequest}
          onRejectRequest={handleRejectRequest}
        />
      )}
      
      {currentView === 'create-project' && (
        <ProjectCreation
          user={currentUser}
          projects={projects}
          accessRequests={accessRequests}
          onNavigate={handleNavigate}
          onCreateProject={handleCreateProject}
          onLogout={handleLogout}
          onApproveRequest={handleApproveRequest}
          onRejectRequest={handleRejectRequest}
        />
      )}

      {currentView === 'project-detail' && selectedProject && (
        <ProjectDetail
          user={currentUser}
          project={selectedProject}
          projects={projects}
          accessRequests={accessRequests}
          onNavigate={handleNavigate}
          onLogout={handleLogout}
          onRequestAccess={handleRequestAccess}
          onApproveRequest={handleApproveRequest}
          onRejectRequest={handleRejectRequest}
        />
      )}

      {currentView === 'profile' && (
        <Profile
          user={currentUser}
          projects={projects}
          accessRequests={accessRequests}
          onNavigate={handleNavigate}
          onLogout={handleLogout}
          onApproveRequest={handleApproveRequest}
          onRejectRequest={handleRejectRequest}
        />
      )}

      {currentView === 'settings' && (
        <Settings
          user={currentUser}
          projects={projects}
          accessRequests={accessRequests}
          onNavigate={handleNavigate}
          onLogout={handleLogout}
          onApproveRequest={handleApproveRequest}
          onRejectRequest={handleRejectRequest}
        />
      )}
    </div>
  );
}

export default App;