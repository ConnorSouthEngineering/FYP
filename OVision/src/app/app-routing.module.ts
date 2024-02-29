import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SessionsComponent } from './sessions/sessions.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ReportComponent } from './reports/report/report.component';
import { ReportsComponent } from './reports/reports.component';
import { LineGraphComponent } from './reports/graphs/line-graph/line-graph.component';
import { TargetComponent } from './targets/targets.component';
const routes: Routes = [
  { path: 'sessions', component: SessionsComponent },
  { path: 'login', component: LoginComponent },
  { path: 'home', component: HomeComponent },
  { path: 'reports', component: ReportsComponent },
  { path: 'report/:reportID', component: ReportComponent },
  { path: 'linegraph', component: LineGraphComponent },
  { path: 'targets', component: TargetComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
