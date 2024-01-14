import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SessionsComponent } from './sessions/sessions.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ReportComponent } from './reports/report/report.component';
import { LineGraphComponent } from './reports/graphs/line-graph/line-graph.component';
const routes: Routes = [
  { path: 'sessions', component: SessionsComponent },
  { path: 'login', component: LoginComponent },
  { path: 'home', component: HomeComponent },
  { path: 'report', component: ReportComponent },
  { path: 'linegraph', component: LineGraphComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
