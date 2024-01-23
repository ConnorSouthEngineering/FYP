export class DataSet 
{
  constructor(
    public actionName: string,
    public dateValues: Array<number>,
    public values: Array<number>
              ) {}
}
export class CountSet extends DataSet 
{
  constructor(
    actionName: string,
    dateValues: Array<number>,
    values: Array<number>
    ){
    super(actionName,dateValues, values)
    }
}
export class TimeSet extends DataSet 
{
  constructor(
    actionName: string,
    dateValues: Array<number>,
    values: Array<number>,
    public timeUnit: string){
    super(actionName,dateValues, values)
  }
}
