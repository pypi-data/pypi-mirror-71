def attribute(name, value, overwrite=False):
    xml ="""
    <Attribute Name="{Name}" Value="{Value}" {overwrite}/>
    """
    return xml.format(Name=name, Value=value, overwrite='Override="true"' if overwrite else "")


def deployment_path(deploy_path, cloud_provider):
    xml = """
        <DeploymentPath Name="{dn}" Default="false">
        <DeploymentService Name="{dsn}" CloudProvider="{cp}">
        <Attributes>
        {DeployAttributes}
        </Attributes>
        </DeploymentService>
        </DeploymentPath>
    """
    return xml.format(DeployAttributes="\n".join([attribute(x, y, True) for x, y in deploy_path['attributes'].iteritems()]),
                      cp=cloud_provider, dn=deploy_path['name'], dsn=deploy_path['service_name'])


def deployment_paths(deploy_paths, cloud_provider):
    xml = """
    {DeployPaths}
"""
    return xml.format(DeployPaths="\n".join([deployment_path(x, cloud_provider) for x in deploy_paths]))


def app_resource(attributes, model, driver):
    xml = """
        <AppResources>
      <AppResource ModelName="{model}" Driver="{driver}">
        <Attributes>
          {Attributes}
        </Attributes>
      </AppResource>
    </AppResources>
    
    """
    return xml.format(Attributes="\n".join(attribute(x, y, True) for x, y in attributes.iteritems()), model=model, driver=driver)


def app_resource_info(app_name, deploy_paths, app_attributes, model, driver, cloud_provider, image_name):
    xml = """
  <AppResourceInfo Name="{AppName}" ImagePath="{img}">
    {AppResource}
    <DeploymentPaths>
    {DeploymentPath}
    
    </DeploymentPaths>
    </AppResourceInfo>
    """
    return xml.format(AppName=app_name, img=image_name, AppResource=app_resource(app_attributes, model, driver), DeploymentPath=deployment_paths(deploy_paths, cloud_provider))


def add_category(category):
    xml = """
    <Category>{Category}</Category>
    """
    return xml.format(Category=category)


def categories_info(categories):
    xml = """
      <Categories>
        {Categories}
  </Categories>
    
    """
    return xml.format(Categories="\n".join([add_category(x) for x in categories]))


def app_template(app_name, deploy_paths, categories, app_attributes, model, driver, cloud_provider, image_name):
    """

    :return:
    """
    xml ="""<?xml version="1.0" encoding="utf-8"?>
<AppTemplateInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    {AppResourceInfo}

        {Categories}
    </AppTemplateInfo>
    """
    app_resource = app_resource_info(app_name, deploy_paths, app_attributes, model, driver, cloud_provider, image_name)
    categories = categories_info(categories)

    return xml.format(AppResourceInfo=app_resource, Categories=categories if categories else "")


dep1 = dict()
dep1['name'] = 'dep1'
dep1['service_name'] = 'service1'
dep1_attrs = dict()
dep1_attrs['attrib1'] = 'value1'
dep1_attrs['attrib2'] = 'value2'
dep1_attrs['attrib3'] = 'value3'
dep1['attributes'] = dep1_attrs

dep2 = dict()
dep2['name'] = 'dep2'
dep2['service_name'] = 'service2'
dep2_attrs = dict()
dep2_attrs['attrib21'] = 'value21'
dep2_attrs['attrib22'] = 'value22'
dep2_attrs['attrib23'] = 'value23'
dep2['attributes'] = dep2_attrs

deploy_paths = [dep1, dep2]

app_attributes = dict()
app_attributes['attr1'] = 'value1'
app_attributes['attr2'] = 'value2'
app_attributes['attr3'] = 'value3'

print app_template('test app', deploy_paths, ['Applications'], app_attributes, 'testmodel', 'testdriver', 'cp1', 'testimage')
#print deployment_paths(deploy_paths, 'cp1')
