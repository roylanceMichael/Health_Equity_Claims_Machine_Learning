-- create the tables, if they don't exist
if not exists(select * from sys.tables where name = 'Balance')
begin
    create table Balance(
		NewMemberID varchar(50),
		CachedBalance varchar(50)
	)
end
if not exists(select * from sys.tables where name = 'Claim')
begin
    create table Claim(
		NewClaimID varchar(50),
		NewMemberID varchar(50),
		DependentServiced varchar(50),
		ClaimType varchar(50),
		DateReceived varchar(50),
		DateProcessed varchar(50),
		ServiceStart varchar(50),
		ServiceEnd varchar(50),
		RepricedAmount varchar(50),
		PatientResponsibilityAmount varchar(50),
	)
end
if not exists(select * from sys.tables where name = 'ClaimDetail')
begin
    create table ClaimDetail(
		NewClaimID varchar(50),
		CPTCode varchar(50)
	)
end
if not exists(select * from sys.tables where name = 'ContributionAndPayment')
begin
    create table ContributionAndPayment(
		NewMemberID varchar(50),
		Amount varchar(50),
		Category varchar(50),
		PaymentAvailableDate varchar(50)
	)
end
if not exists(select * from sys.tables where name = 'Dependent')
begin
    create table Dependent(
		NewMemberID varchar(50),
		DependentID varchar(50),
		Relationship varchar(50),
		BirthYear varchar(50),
		Gender varchar(50),
		State varchar(50),
		Zip varchar(50)
	)
end
if not exists(select * from sys.tables where name = 'Member')
begin
    create table Member(
		NewMemberID varchar(50),
		State varchar(50),
		Zip varchar(50),
		Gender varchar(50),
		BirthYear varchar(50),
		State varchar(50),
		HsaEffectiveDate varchar(50)
	)
end