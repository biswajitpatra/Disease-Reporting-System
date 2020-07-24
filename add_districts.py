from django.contrib.auth.models import User, Group

from disdata.models import Pincode,District

if(Group.objects.filter(name='district official').exists()==False):
    gp = Group.objects.create(name='district official')

gp = Group.objects.get(name='district official')

states = [21,2,40]


for p in Pincode.objects.all():  
    p.province = p.province.lower()
    if p.state_code in states: 
        if(District.objects.filter(name=p.province).exists()==False):
            u = User.objects.create_user(username=p.province+"@123",email=p.province+"@gov.com",password="gocoronago")
            d = District.objects.create(name=p.province,district_official=u,rainfall=0.0,altitude=20,temprature=0,population=0,water_source=0,humidity=0.0,age_frequency_vector=[0,0,0],slums_count=0,wind=0,victim_ids=['pt'])
            p.district = d
            u.is_staff =True
            u.save()
            gp.user_set.add(u)
        p.save()
    else:
        p.delete()


for p in Pincode.objects.all():
    p.district = District.objects.get(name=p.province)
    p.save()


# for p in Pincode.objects.all():
#     if(p.state_code not in states):
#         try:
#             u = User.objects.get(username=p.province+"@123")
#             u.delete()
#         except:
#             print("User does not exist")
#         p.delete()
#     else:
#         p.district = District.objects.get(name=p.province) 
#         p.save()

# for u in User.objects.all():
#     u.is_staff=True
#     u.save()
