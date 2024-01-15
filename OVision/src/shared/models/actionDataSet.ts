export class actionDataSet {
    constructor(public actionName: string, public dateValues: Array<Date>, public metricType: string, public metricValue: Array<number>, public metricUnit: string | null) {}
  }