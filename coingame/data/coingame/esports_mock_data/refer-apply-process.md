#### 1 推广专区 推广资格页面初始化
```
POST /refer/apply/findUserTotalExp HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NDA0MTA2NzYsInVzZXJfbmFtZSI6IjEwMDAiLCJqdGkiOiJmYzYyMTE2Yy03MTJkLTQ0MTktODJkYi02Y2Y1MGM2NmFhYjgiLCJjbGllbnRfaWQiOiJicm93c2VyIiwic2NvcGUiOlsidWkiXX0.SzInwwA8G_wbhptPKMU6NudjW_8WFNbDWeQS2cDiPwA
```
返回消息体参数描述

| 字段       | 描述                   |
     | ---------- | ---------------------- |
     | bonusPoints         | 用户经验  |
     | bonusPointsPercent         | 用户经验百分比  |
     | crmReachReferBonusPoints         | 达标经验  |
     | status      | 状态   REVOKED:身份撤销的  GRANTED:身份启用的 //NOT_REFER :不是推广员 
     
     返回json示例：
         json
     {  "bonusPoints":"3",
         "bonusPointsPercent":"1%",
         "crmReachReferBonusPoints":"190",
         "status":"NOT_REFER" 
        }

#### 2 推广专区 发送短信
```
  POST /vcode/referral-register HTTP/1.1
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NDA0MTA2NzYsInVzZXJfbmFtZSI6IjEwMDAiLCJqdGkiOiJmYzYyMTE2Yy03MTJkLTQ0MTktODJkYi02Y2Y1MGM2NmFhYjgiLCJjbGllbnRfaWQiOiJicm93c2VyIiwic2NvcGUiOlsidWkiXX0.SzInwwA8G_wbhptPKMU6NudjW_8WFNbDWeQS2cDiPwA
  Accept-Language: en
  ```
    
    
#### 3 推广专区 短信验证
  ```
  POST /refer/apply/referral-register HTTP/1.1
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NDA0MTA2NzYsInVzZXJfbmFtZSI6IjEwMDAiLCJqdGkiOiJmYzYyMTE2Yy03MTJkLTQ0MTktODJkYi02Y2Y1MGM2NmFhYjgiLCJjbGllbnRfaWQiOiJicm93c2VyIiwic2NvcGUiOlsidWkiXX0.SzInwwA8G_wbhptPKMU6NudjW_8WFNbDWeQS2cDiPwA
  ```
报文请求体

| 字段       | 描述                   | 
| ---------- | ---------------------- |
| vcode       |验证码 |

请求体示例：
```json
{
	"vcode":"123456"
}
```
返回消息体参数描述

true：验证码通过
false:验证码不通过





         
```