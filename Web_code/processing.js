function PVector(x, y, z) {
    this.x = x || 0;
    this.y = y || 0;
    this.z = z || 0;
  }

 PVector.lerp = function(v1, v2, amt) {
    // non-static lerp mutates object, but this version returns a new vector
    var retval = new PVector(v1.x, v1.y, v1.z);
    retval.lerp(v2, amt);
    return retval;
  };