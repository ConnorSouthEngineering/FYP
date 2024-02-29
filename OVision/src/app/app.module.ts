import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgxEchartsModule } from 'ngx-echarts';
import * as echarts from 'echarts';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PaginationComponent } from './pagination/pagination.component';
import { SessionsComponent } from './sessions/sessions.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ReportComponent } from './reports/report/report.component';
import { ReportsComponent } from './reports/reports.component';
import { LineGraphComponent } from './reports/graphs/line-graph/line-graph.component';
import { BarGraphComponent } from './reports/graphs/bar-graph/bar-graph.component';
import { TargetComponent } from './targets/targets.component';

@NgModule({
  declarations: [
    AppComponent,
    PaginationComponent,
    SessionsComponent,
    LoginComponent,
    HomeComponent,
    ReportComponent,
    ReportsComponent,
    LineGraphComponent,
    BarGraphComponent,
    TargetComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxEchartsModule.forRoot({
      echarts,
    }),
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
