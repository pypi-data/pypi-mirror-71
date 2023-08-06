
class VersionException(Exception):
    def __init__(self, message):
        self.message = message


class Version():
    
    def __init__(self, value):
        if isinstance(value, Version):
            self._major = value._major
            self._minor = value._minor
            self._revision = value._revision
            self._build = value._build
            self._dev = value._dev
        else:
            self._major = None
            self._minor = None
            self._revision = None
            self._build = None
            self._dev = False
            
            version = value

            # extract build number
            if '-' in value:
                s = value.split('-', 1)
                self._build = s[1]
                value = s[0]
            
            if '.' in value:
                s = value.split('.')
                
                if(len(s)>3):
                    raise VersionException(f"Invalid version {version}")
                    
                try:
                    if len(s)==3:
                        self._major = int(s[0])
                        self._minor = int(s[1])
                        self._revision = int(s[2])
                    elif len(s)==2:
                        self._major = int(s[0])
                        self._minor = int(s[1])
                except Exception as e:
                    raise VersionException(f"Invalid version {version}")
                    
            else:
                try:
                    self._major = int(value)
                except Exception as e:
                    raise VersionException(f"Invalid version {version}")
            
            if self._build and ( self._major is None or self._minor is None or self._revision is None):
                raise VersionException(f"Invalid version {version}")
            elif self._build and self._build=="dev":
                self._dev = True
        
    def compare(self, version):
        l = [self._major, self._minor, self._revision, self._build]
        r = [version._major, version._minor, version._revision, version._build]
        
        if self._dev and version._dev:
            return 0
        elif self._dev and not version._dev:
            return -1
        elif not self._dev and version._dev:
            return 1
        
        res = 0
        for i in range(3):
            if res==0:
                if l[i] is None or r[i] is None:
                    res = 0
                elif l[i] is not None and r[i] is not None:
                    if l[i]<r[i]:
                        res = -1
                    if l[i]>r[i]:
                        res = 1
                
        if l[3] is not None and r[3] is None:
            return -1
        if l[3] is None and r[3] is not None:
            return 1
        if l[3] is not None and r[3] is not None:
            if l[3]<r[3]:
                return -1
            elif l[3]==r[3]:
                return 0
            elif l[3]>r[3]:
                return 1

        return res
    
    def __str__(self):
        version = f"{self._major}"
        if self._minor is not None:
            version += f".{self._minor}"
        if self._revision is not None:
            version += f".{self._revision}"
        if self._build is not None:
            version += f"-{self._build}"
        return version
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.compare(other)==0
    
    def __lt__(self, other):
        return self.compare(other)<0

    def __le__(self, other):
        return self.compare(other)<=0

class VersionRange(object):
    def __init__(self, value, versions={}):
        self._tree = {} # for future parsing 
        self._value = value
        self._versions = versions

        self.parse(value)
    
        
    def parse(self, value):
        if value=='latest':
            return
        else:
            Version(value)
    
    @property
    def value(self):
        if self._value=='latest':
            if len(self._versions)==0:
                raise VersionException(f"no version range specified")
            max = Version(self._versions[0])
            for version in self._versions:
                if Version(version)>max:
                    max = Version(version)
            return max
        else:
            return Version(self._value)
    
    def add_version(self, value):
        self._versions.append(value)
    
    def match(self, value):
        if Version(value)==self.value():
            return True
        else:
            for version in self._versions:
                if Version(version)==Version(value):
                    return True
        return False
    
    def __str__(self):
        return str(self.value())
    
    def __repr__(self):
        return self.__str__()
