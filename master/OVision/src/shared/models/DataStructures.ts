export class DataSet 
{
  constructor(
    public classid: number,
    public dateValues: Array<string>,
    public values: Array<number>
              ) {}
}
export class CountSet extends DataSet 
{
  constructor(
    classid: number,
    dateValues: Array<string>,
    values: Array<number>
    ){
    super(classid,dateValues, values)
    }
}
export class TimeSet extends DataSet 
{
  constructor(
    classid: number,
    dateValues: Array<string>,
    values: Array<number>,
    public metric: string){
    super(classid,dateValues, values)
  }
}
