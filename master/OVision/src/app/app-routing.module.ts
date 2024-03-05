import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SessionsComponent } from './sessions/sessions.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ReportComponent } from './reports/report/report.component';
import { ReportsComponent } from './reports/reports.component';
import { LineGraphComponent } from './reports/graphs/line-graph/line-graph.component';
import { BarGraphComponent } from './reports/graphs/bar-graph/bar-graph.component';
import { TargetComponent } from './targets/targets.component';
import { CreateTargetComponent } from './targets/create-target/create-target.component';
import { ModelsComponent } from './models/models.component';
import { CreateModelsComponent } from './models/create-models/create-models.component';
const routes: Routes = [
  { path: 'sessions', component: SessionsComponent },
  { path: 'login', component: LoginComponent },
  { path: 'home', component: HomeComponent },
  { path: 'reports', component: ReportsComponent },
  { path: 'report/:reportID', component: ReportComponent },
  { path: 'linegraph', component: LineGraphComponent },
  { path: 'bargraph', component: BarGraphComponent },
  { path: 'targets/view', component: TargetComponent },
  { path: 'targets/create', component: CreateTargetComponent },
  { path: 'models/view', component: ModelsComponent },
  { path: 'models/create', component: CreateModelsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }